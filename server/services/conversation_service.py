"""Service layer for conversation operations."""
from datetime import datetime
from typing import List, Dict, Any
from uuid import UUID

from models.conversation import Conversation
from models.message import Message
from models.user import User


async def create_conversation(user_ids: List[UUID]) -> Conversation:
    """
    Create a new conversation with specified participants.
    
    Args:
        user_ids: List of user UUIDs to include in the conversation
        
    Returns:
        Created Conversation object
    """
    conv = Conversation(
        participants=user_ids,
        created_at=datetime.now(),
        last_message_at=datetime.now(),
    )
    await conv.insert()
    return conv


async def create_message(sender_id: UUID, conversation_id: UUID, content: str) -> Message:
    """
    Create a new message in a conversation.
    
    Args:
        sender_id: UUID of the message sender
        conversation_id: UUID of the conversation
        content: Message content text
        
    Returns:
        Created Message object
    """
    msg = Message(
        conversation_id=conversation_id,
        sender_id=sender_id,
        content=content,
        timestamp=datetime.now()
    )
    await msg.insert()
    
    # Update conversation's last message info
    conv = await Conversation.get(conversation_id)
    if conv:
        conv.last_message = content
        conv.last_message_at = datetime.now()
        await conv.save()
    
    return msg


async def get_conversation_messages(conversation_id: UUID) -> List[Message]:
    """
    Get all messages in a conversation, sorted by timestamp.
    
    Args:
        conversation_id: UUID of the conversation
        
    Returns:
        List of Message objects
    """
    messages = await Message.find(
        Message.conversation_id == conversation_id
    ).sort("+timestamp").to_list()
    return messages


async def get_user_conversations(user_id: UUID) -> List[Dict[str, Any]]:
    """
    Get all conversations for a user with participant details and unread counts.
    Optimized with batch queries to prevent N+1 problem.
    
    Args:
        user_id: UUID of the user
        
    Returns:
        List of conversation dictionaries with full participant info
    """
    convs = await Conversation.find(
        {"participants": user_id}
    ).sort("-last_message_at").to_list()
    
    if not convs:
        return []
    
    # Collect all unique participant IDs and conversation IDs
    participant_ids = set()
    conversation_ids = []
    
    for conv in convs:
        conversation_ids.append(conv.id)
        participant_ids.update(conv.participants)
    
    # ✅ BATCH QUERY 1: Get all participants in ONE query
    users = await User.find({
        "_id": {"$in": list(participant_ids)}
    }).to_list()
    users_map = {user.id: user for user in users}
    
    # ✅ BATCH QUERY 2: Get all unread messages for all conversations in ONE query
    unread_messages = await Message.find({
        "conversation_id": {"$in": conversation_ids},
        "sender_id": {"$ne": user_id},
        "is_read": False
    }).to_list()
    
    # Count unread messages per conversation
    unread_counts = {}
    for msg in unread_messages:
        conv_id = msg.conversation_id
        unread_counts[conv_id] = unread_counts.get(conv_id, 0) + 1
    
    # Build results using the cached data
    results = []
    for conv in convs:
        # Get participant details from cache
        participants_info = []
        for participant_id in conv.participants:
            user = users_map.get(participant_id)
            if user:
                participants_info.append({
                    "id": user.id,
                    "username": user.username,
                    "fullname": user.fullname,
                    "status": user.status,
                    "last_online": user.last_online
                })
        
        results.append({
            "id": conv.id,
            "participants": participants_info,
            "created_at": conv.created_at,
            "last_message_at": conv.last_message_at,
            "last_message": conv.last_message,
            "unread_count": unread_counts.get(conv.id, 0)
        })
    
    return results


async def mark_messages_as_read(conversation_id: UUID, user_id: UUID) -> int:
    """
    Mark all messages in a conversation as read for a user.
    
    Args:
        conversation_id: UUID of the conversation
        user_id: UUID of the user marking messages as read
        
    Returns:
        Number of messages marked as read
    """
    messages = await Message.find(
        Message.conversation_id == conversation_id,
        Message.sender_id != user_id,
        Message.is_read == False
    ).to_list()
    
    count = 0
    for msg in messages:
        msg.is_read = True
        msg.read_at = datetime.now()
        await msg.save()
        count += 1
    
    return count


async def delete_conversation(conversation_id: UUID, user_id: UUID) -> None:
    """
    Delete a conversation and all its messages.
    
    Args:
        conversation_id: UUID of the conversation
        user_id: UUID of the user deleting (must be participant)
    """
    conv = await Conversation.get(conversation_id)
    if not conv or user_id not in conv.participants:
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this conversation"
        )
    
    # Delete all messages
    messages = await Message.find(Message.conversation_id == conversation_id).to_list()
    for msg in messages:
        await msg.delete()
    
    # Delete conversation
    await conv.delete()


async def get_conversation_between_users(user_id_1: UUID, user_id_2: UUID) -> Conversation | None:
    """
    Find existing conversation between two users.
    
    Args:
        user_id_1: First user UUID
        user_id_2: Second user UUID
        
    Returns:
        Conversation if exists, None otherwise
    """
    conv = await Conversation.find_one({
        "participants": {"$all": [user_id_1, user_id_2], "$size": 2}
    })
    return conv


async def get_conversation_messages_paginated(
    conversation_id: UUID,
    skip: int = 0,
    limit: int = 50
) -> tuple[List[Message], int]:
    """
    Get paginated messages in a conversation.
    
    Args:
        conversation_id: UUID of the conversation
        skip: Number of messages to skip
        limit: Maximum number of messages to return
        
    Returns:
        Tuple of (messages list, total count)
    """
    # Get total count
    total = await Message.find(
        Message.conversation_id == conversation_id
    ).count()
    
    # Get paginated messages (newest first, then reverse for display)
    messages = await Message.find(
        Message.conversation_id == conversation_id
    ).sort("-timestamp").skip(skip).limit(limit).to_list()
    
    # Reverse to show oldest first in the page
    messages.reverse()
    
    return messages, total
