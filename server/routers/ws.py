"""WebSocket endpoints for real-time chat functionality."""
from uuid import UUID
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, status
from typing import Dict, Any
import logging

from core.websocket_manager import connection_manager
from models.conversation import Conversation
from models.message import Message
from models.user import User
from utils.jwt import decode_token

router = APIRouter(prefix="/ws", tags=["WebSocket"])
logger = logging.getLogger(__name__)


async def get_current_user_ws(websocket: WebSocket) -> User | None:
    """Authenticate WebSocket connection using query parameter token."""
    token = websocket.query_params.get("token")
    if not token:
        return None
    
    try:
        payload = decode_token(token)
        user_id = UUID(payload.get("sub"))
        user = await User.get(user_id)
        return user
    except Exception as e:
        logger.error(f"WebSocket authentication error: {e}")
        return None


@router.websocket("/chat")
async def websocket_chat_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time chat.
    
    Connection: ws://localhost:8000/ws/chat?token=<access_token>
    
    Expected message formats:
    - Send message: {"type": "message", "conversation_id": "uuid", "content": "text"}
    - Mark as read: {"type": "read", "message_id": "uuid"}
    - Typing indicator: {"type": "typing", "conversation_id": "uuid", "is_typing": true}
    """
    # Authenticate user
    user = await get_current_user_ws(websocket)
    if not user:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    
    # Connect user
    await connection_manager.connect(user.id, websocket)
    
    # Update user status to online
    user.status = "online"
    await user.save()
    
    try:
        # Send connection confirmation
        await websocket.send_json({
            "type": "connected",
            "user_id": str(user.id),
            "message": "Connected successfully"
        })
        
        # Listen for messages
        while True:
            data = await websocket.receive_json()
            await handle_websocket_message(data, user, websocket)
            
    except WebSocketDisconnect:
        logger.info(f"User {user.id} disconnected")
    except Exception as e:
        logger.error(f"WebSocket error for user {user.id}: {e}")
    finally:
        # Disconnect user
        connection_manager.disconnect(user.id, websocket)
        
        # Update user status to offline if no more connections
        if not connection_manager.is_user_online(user.id):
            user.status = "offline"
            await user.save()


async def handle_websocket_message(data: Dict[str, Any], user: User, websocket: WebSocket):
    """Handle different types of WebSocket messages."""
    message_type = data.get("type")
    
    if message_type == "message":
        await handle_chat_message(data, user)
    elif message_type == "read":
        await handle_read_receipt(data, user)
    elif message_type == "typing":
        await handle_typing_indicator(data, user)
    else:
        await websocket.send_json({
            "type": "error",
            "message": f"Unknown message type: {message_type}"
        })


async def handle_chat_message(data: Dict[str, Any], user: User):
    """Handle incoming chat message."""
    try:
        conversation_id = UUID(data.get("conversation_id"))
        content = data.get("content", "").strip()
        
        if not content:
            return
        
        # Verify user is participant
        conversation = await Conversation.get(conversation_id)
        if not conversation or user.id not in conversation.participants:
            logger.warning(f"User {user.id} not authorized for conversation {conversation_id}")
            return
        
        # Create message
        message = Message(
            conversation_id=conversation_id,
            sender_id=user.id,
            content=content
        )
        await message.insert()
        
        # Update conversation
        conversation.last_message = content
        conversation.last_message_at = message.timestamp
        await conversation.save()
        
        # Broadcast to all participants
        broadcast_data = {
            "type": "message",
            "message_id": str(message.id),
            "conversation_id": str(conversation_id),
            "sender_id": str(user.id),
            "sender_username": user.username,
            "sender_fullname": user.fullname,
            "content": content,
            "timestamp": message.timestamp.isoformat(),
            "is_read": False
        }
        
        await connection_manager.broadcast_to_conversation(
            broadcast_data,
            conversation_id,
            conversation.participants
        )
        
        logger.info(f"Message sent in conversation {conversation_id} by user {user.id}")
        
    except Exception as e:
        logger.error(f"Error handling chat message: {e}")


async def handle_read_receipt(data: Dict[str, Any], user: User):
    """Handle message read receipt."""
    try:
        message_id = UUID(data.get("message_id"))
        
        # Get and update message
        message = await Message.get(message_id)
        if not message or message.sender_id == user.id:
            return
        
        message.is_read = True
        from datetime import datetime
        message.read_at = datetime.now()
        await message.save()
        
        # Notify sender
        await connection_manager.send_personal_message(
            {
                "type": "read_receipt",
                "message_id": str(message_id),
                "reader_id": str(user.id),
                "read_at": message.read_at.isoformat()
            },
            message.sender_id
        )
        
        logger.info(f"Message {message_id} marked as read by user {user.id}")
        
    except Exception as e:
        logger.error(f"Error handling read receipt: {e}")


async def handle_typing_indicator(data: Dict[str, Any], user: User):
    """Handle typing indicator."""
    try:
        conversation_id = UUID(data.get("conversation_id"))
        is_typing = data.get("is_typing", False)
        
        # Verify user is participant
        conversation = await Conversation.get(conversation_id)
        if not conversation or user.id not in conversation.participants:
            return
        
        # Broadcast typing indicator to other participants
        await connection_manager.broadcast_to_conversation(
            {
                "type": "typing",
                "conversation_id": str(conversation_id),
                "user_id": str(user.id),
                "username": user.username,
                "is_typing": is_typing
            },
            conversation_id,
            conversation.participants,
            exclude_user_id=user.id
        )
        
    except Exception as e:
        logger.error(f"Error handling typing indicator: {e}")


# Removed /ws/online-users endpoint for security reasons
# Users should use GET /users/friends/online instead to see their online friends
# This prevents privacy issues from exposing all online users

