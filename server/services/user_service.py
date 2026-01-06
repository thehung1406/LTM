"""Service layer for user operations."""
from typing import List
from uuid import UUID
from fastapi import HTTPException, status

from models.user import User
from schemas.user import UserCreate, UserRead, UserUpdate
from utils.security import hash_password, verify_password


async def list_users(offset: int = 0, limit: int = 50) -> List[UserRead]:
    """
    Get a paginated list of users.
    
    Args:
        offset: Number of users to skip
        limit: Maximum number of users to return
        
    Returns:
        List of UserRead objects
    """
    users = await User.find().skip(offset).limit(limit).to_list()
    return [UserRead(**user.model_dump()) for user in users]


async def get_user_by_id(user_id: str) -> User:
    """
    Get a user by their ID.
    
    Args:
        user_id: UUID string of the user
        
    Returns:
        User object
        
    Raises:
        HTTPException: If user not found
    """
    from uuid import UUID
    user = await User.get(UUID(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


async def create_user(payload: UserCreate) -> User:
    """
    Create a new user.
    
    Args:
        payload: UserCreate schema with user details
        
    Returns:
        Created User object
        
    Raises:
        HTTPException: If username already exists
    """
    existing_user = await User.find_one({"username": payload.username})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )
    
    new_user = User(
        username=payload.username,
        hashed_password=hash_password(payload.password),
        fullname=payload.fullname
    )
    await new_user.insert()
    return new_user


async def change_user_password(user: User, old_password: str, new_password: str) -> User:
    """
    Change a user's password.
    
    Args:
        user: User object
        old_password: Current password for verification
        new_password: New password to set
        
    Returns:
        Updated User object
        
    Raises:
        HTTPException: If old password is incorrect
    """
    if not verify_password(old_password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mật khẩu cũ không đúng"
        )
    
    user.hashed_password = hash_password(new_password)
    await user.save()
    return user


async def update_user_profile(user_id: UUID, payload: UserUpdate) -> User:
    """
    Update user profile information.
    
    Args:
        user_id: UUID of the user
        payload: UserUpdate schema with fields to update
        
    Returns:
        Updated User object
        
    Raises:
        HTTPException: If user not found
    """
    user = await User.get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Update only provided fields
    if payload.fullname is not None:
        user.fullname = payload.fullname
    
    await user.save()
    return user


async def search_users(query: str, limit: int = 10) -> List[UserRead]:
    """
    Search users by username or fullname.
    
    Args:
        query: Search query string
        limit: Maximum number of results
        
    Returns:
        List of matching UserRead objects
    """
    users = await User.find({
        "$or": [
            {"username": {"$regex": query, "$options": "i"}},
            {"fullname": {"$regex": query, "$options": "i"}}
        ]
    }).limit(limit).to_list()
    
    return [UserRead(**user.model_dump()) for user in users]


async def get_user_statistics(user_id: UUID) -> dict:
    """
    Get user statistics (friends count, unread messages, etc).
    
    Args:
        user_id: UUID of the user
        
    Returns:
        Dictionary with user statistics
    """
    from models.friend import Friend, FriendRequestStatus
    from models.conversation import Conversation
    from models.message import Message
    
    # Count total friends
    total_friends = await Friend.find({
        "$or": [
            {"requester_id": user_id},
            {"addressee_id": user_id}
        ],
        "status": FriendRequestStatus.ACCEPTED
    }).count()
    
    # Get online friends
    friendships = await Friend.find({
        "$or": [
            {"requester_id": user_id},
            {"addressee_id": user_id}
        ],
        "status": FriendRequestStatus.ACCEPTED
    }).to_list()
    
    friend_ids = []
    for friendship in friendships:
        friend_id = (
            friendship.addressee_id 
            if friendship.requester_id == user_id 
            else friendship.requester_id
        )
        friend_ids.append(friend_id)
    
    online_friends = 0
    if friend_ids:
        online_friends = await User.find({
            "_id": {"$in": friend_ids},
            "status": "online"
        }).count()
    
    # Count conversations
    total_conversations = await Conversation.find({
        "participants": user_id
    }).count()
    
    # Count unread messages (only in user's conversations)
    # Get all conversation IDs where user is participant
    user_conversations = await Conversation.find({
        "participants": user_id
    }).to_list()
    
    conversation_ids = [conv.id for conv in user_conversations]
    
    # Count unread messages only in these conversations
    unread_messages = 0
    if conversation_ids:
        unread_messages = await Message.find({
            "conversation_id": {"$in": conversation_ids},
            "sender_id": {"$ne": user_id},
            "is_read": False
        }).count()
    
    return {
        "total_friends": total_friends,
        "online_friends": online_friends,
        "total_conversations": total_conversations,
        "unread_messages": unread_messages
    }
