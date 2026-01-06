"""Chat and conversation management endpoints."""
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query

from models.conversation import Conversation
from models.user import User
from schemas.conversation import (
    ConversationCreate,
    ConversationResponse,
    ConversationDetailResponse,
    ParticipantInfo
)
from schemas.message import MessageCreate, MessageResponse
from services.conversation_service import (
    create_conversation,
    create_message,
    get_conversation_messages_paginated,
    get_user_conversations,
    mark_messages_as_read,
    delete_conversation,
    get_conversation_between_users
)
from utils.dependencies import get_current_user

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/conversations", response_model=ConversationResponse, status_code=status.HTTP_201_CREATED)
async def create_new_conversation(
    data: ConversationCreate,
    current_user: User = Depends(get_current_user)
):
    """Create a new conversation with another user (returns existing if already exists)."""
    # Check if other user exists
    other_user = await User.get(data.participant_id)
    if not other_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check if conversation already exists
    existing_conv = await get_conversation_between_users(current_user.id, data.participant_id)
    
    if existing_conv:
        # Return existing conversation with full participant info
        unread_count = await get_unread_count(existing_conv.id, current_user.id)
        participants_info = [
            ParticipantInfo(
                id=current_user.id,
                username=current_user.username,
                fullname=current_user.fullname,
                status=current_user.status,
                last_online=current_user.last_online
            ),
            ParticipantInfo(
                id=other_user.id,
                username=other_user.username,
                fullname=other_user.fullname,
                status=other_user.status,
                last_online=other_user.last_online
            )
        ]
        return ConversationResponse(
            id=existing_conv.id,
            participants=participants_info,
            created_at=existing_conv.created_at,
            last_message_at=existing_conv.last_message_at,
            last_message=existing_conv.last_message,
            unread_count=unread_count
        )
    
    # Create new conversation
    participants = [current_user.id, data.participant_id]
    conv = await create_conversation(participants)
    
    participants_info = [
        ParticipantInfo(
            id=current_user.id,
            username=current_user.username,
            fullname=current_user.fullname,
            status=current_user.status,
            last_online=current_user.last_online
        ),
        ParticipantInfo(
            id=other_user.id,
            username=other_user.username,
            fullname=other_user.fullname,
            status=other_user.status,
            last_online=other_user.last_online
        )
    ]
    
    return ConversationResponse(
        id=conv.id,
        participants=participants_info,
        created_at=conv.created_at,
        last_message_at=conv.last_message_at,
        last_message=conv.last_message,
        unread_count=0
    )


@router.get("/conversations", response_model=List[ConversationResponse])
async def list_user_conversations(current_user: User = Depends(get_current_user)):
    """Get all conversations for the current user."""
    convs = await get_user_conversations(current_user.id)
    return [ConversationResponse(**c) for c in convs]


@router.get("/conversations/with/{user_id}", response_model=ConversationResponse | None)
async def get_conversation_with_user(
    user_id: UUID,
    current_user: User = Depends(get_current_user)
):
    """Get existing conversation with a specific user (or null if none exists)."""
    conv = await get_conversation_between_users(current_user.id, user_id)
    
    if not conv:
        return None
    
    # Get participant info
    other_user = await User.get(user_id)
    if not other_user:
        return None
    
    unread_count = await get_unread_count(conv.id, current_user.id)
    
    participants_info = [
        ParticipantInfo(
            id=current_user.id,
            username=current_user.username,
            fullname=current_user.fullname,
            status=current_user.status,
            last_online=current_user.last_online
        ),
        ParticipantInfo(
            id=other_user.id,
            username=other_user.username,
            fullname=other_user.fullname,
            status=other_user.status,
            last_online=other_user.last_online
        )
    ]
    
    return ConversationResponse(
        id=conv.id,
        participants=participants_info,
        created_at=conv.created_at,
        last_message_at=conv.last_message_at,
        last_message=conv.last_message,
        unread_count=unread_count
    )


@router.get("/conversations/{conversation_id}", response_model=ConversationDetailResponse)
async def get_conversation_details(
    conversation_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_user)
):
    """Get detailed information about a conversation including paginated messages."""
    conv = await Conversation.get(conversation_id)
    
    if not conv:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    if current_user.id not in conv.participants:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this conversation"
        )
    
    # Get paginated messages
    messages, total = await get_conversation_messages_paginated(conversation_id, skip, limit)
    
    # Get participant info
    participants_info = []
    for participant_id in conv.participants:
        user = await User.get(participant_id)
        if user:
            participants_info.append(
                ParticipantInfo(
                    id=user.id,
                    username=user.username,
                    fullname=user.fullname,
                    status=user.status,
                    last_online=user.last_online
                )
            )
    
    return ConversationDetailResponse(
        id=conv.id,
        participants=participants_info,
        created_at=conv.created_at,
        messages=[
            MessageResponse(
                id=m.id,
                conversation_id=m.conversation_id,
                sender_id=m.sender_id,
                content=m.content,
                timestamp=m.timestamp,
                is_read=m.is_read,
                read_at=m.read_at
            )
            for m in messages
        ],
        total_messages=total
    )


@router.post("/conversations/{conversation_id}/messages", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def send_chat_message(
    conversation_id: UUID,
    data: MessageCreate,
    current_user: User = Depends(get_current_user)
):
    """Send a message in a conversation (REST endpoint, prefer WebSocket for real-time)."""
    # Verify user is participant
    conv = await Conversation.get(conversation_id)
    
    if not conv:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    if current_user.id not in conv.participants:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to send messages in this conversation"
        )
    
    # Create message
    msg = await create_message(current_user.id, conversation_id, data.content)
    
    return MessageResponse(
        id=msg.id,
        conversation_id=msg.conversation_id,
        sender_id=msg.sender_id,
        content=msg.content,
        timestamp=msg.timestamp,
        is_read=msg.is_read,
        read_at=msg.read_at
    )


@router.post("/conversations/{conversation_id}/read", status_code=status.HTTP_204_NO_CONTENT)
async def mark_conversation_as_read(
    conversation_id: UUID,
    current_user: User = Depends(get_current_user)
):
    """Mark all messages in a conversation as read."""
    # Verify user is participant
    conv = await Conversation.get(conversation_id)
    
    if not conv:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    if current_user.id not in conv.participants:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this conversation"
        )
    
    await mark_messages_as_read(conversation_id, current_user.id)


@router.delete("/conversations/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_conversation_endpoint(
    conversation_id: UUID,
    current_user: User = Depends(get_current_user)
):
    """Delete a conversation and all its messages."""
    await delete_conversation(conversation_id, current_user.id)


async def get_unread_count(conversation_id: UUID, user_id: UUID) -> int:
    """Helper function to get unread message count."""
    from models.message import Message
    return await Message.find(
        Message.conversation_id == conversation_id,
        Message.sender_id != user_id,
        Message.is_read == False
    ).count()

