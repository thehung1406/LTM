"""Service layer for friend operations."""
from datetime import datetime
from uuid import UUID
from typing import List
from fastapi import HTTPException, status

from models.friend import Friend, FriendRequestStatus
from models.user import User
from schemas.friend import FriendResponse


async def send_friend_request(requester_id: UUID, addressee_id: UUID) -> Friend:
    """Send a friend request to another user."""
    if requester_id == addressee_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot send friend request to yourself"
        )
    
    # Check if addressee exists
    addressee = await User.get(addressee_id)
    if not addressee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check if friend request already exists (either direction)
    existing = await Friend.find_one({
        "$or": [
            {"requester_id": requester_id, "addressee_id": addressee_id},
            {"requester_id": addressee_id, "addressee_id": requester_id}
        ]
    })
    
    if existing:
        if existing.status == FriendRequestStatus.ACCEPTED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Already friends"
            )
        elif existing.status == FriendRequestStatus.PENDING:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Friend request already sent"
            )
        elif existing.status == FriendRequestStatus.BLOCKED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot send friend request"
            )
    
    # Create new friend request
    friend_request = Friend(
        requester_id=requester_id,
        addressee_id=addressee_id,
        status=FriendRequestStatus.PENDING
    )
    await friend_request.insert()
    return friend_request


async def accept_friend_request(request_id: UUID, current_user_id: UUID) -> Friend:
    """Accept a friend request."""
    friend_request = await Friend.get(request_id)
    
    if not friend_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Friend request not found"
        )
    
    # Only the addressee can accept
    if friend_request.addressee_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to accept this request"
        )
    
    if friend_request.status != FriendRequestStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Friend request is not pending"
        )
    
    friend_request.status = FriendRequestStatus.ACCEPTED
    friend_request.updated_at = datetime.now()
    await friend_request.save()
    
    return friend_request


async def reject_friend_request(request_id: UUID, current_user_id: UUID) -> Friend:
    """Reject a friend request."""
    friend_request = await Friend.get(request_id)
    
    if not friend_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Friend request not found"
        )
    
    # Only the addressee can reject
    if friend_request.addressee_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to reject this request"
        )
    
    friend_request.status = FriendRequestStatus.REJECTED
    friend_request.updated_at = datetime.now()
    await friend_request.save()
    
    return friend_request


async def get_friend_requests(user_id: UUID) -> List[Friend]:
    """Get all pending friend requests for a user."""
    requests = await Friend.find(
        Friend.addressee_id == user_id,
        Friend.status == FriendRequestStatus.PENDING
    ).to_list()
    return requests


async def get_friends_list(user_id: UUID) -> List[FriendResponse]:
    """Get all friends for a user with their details (optimized with batch query)."""
    friendships = await Friend.find({
        "$or": [
            {"requester_id": user_id},
            {"addressee_id": user_id}
        ],
        "status": FriendRequestStatus.ACCEPTED
    }).to_list()
    
    if not friendships:
        return []
    
    # Collect all friend IDs
    friend_ids = []
    for friendship in friendships:
        friend_id = (
            friendship.addressee_id 
            if friendship.requester_id == user_id 
            else friendship.requester_id
        )
        friend_ids.append(friend_id)
    
    # ✅ BATCH QUERY: Get all friends in ONE query
    friends_users = await User.find({
        "_id": {"$in": friend_ids}
    }).to_list()
    
    # Create lookup map for O(1) access
    users_map = {user.id: user for user in friends_users}
    
    # Build response list
    friends_list = []
    for friendship in friendships:
        friend_id = (
            friendship.addressee_id 
            if friendship.requester_id == user_id 
            else friendship.requester_id
        )
        
        friend_user = users_map.get(friend_id)
        if friend_user:
            friends_list.append(FriendResponse(
                id=friendship.id,
                friend_id=friend_id,
                friend_username=friend_user.username,
                friend_fullname=friend_user.fullname,
                status=friend_user.status,
                last_online=friend_user.last_online,
                created_at=friendship.created_at
            ))
    
    return friends_list


async def remove_friend(friendship_id: UUID, current_user_id: UUID) -> None:
    """Remove a friend (delete friendship)."""
    friendship = await Friend.get(friendship_id)
    
    if not friendship:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Friendship not found"
        )
    
    # Only participants can remove the friendship
    if current_user_id not in [friendship.requester_id, friendship.addressee_id]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to remove this friendship"
        )
    
    await friendship.delete()


async def block_user(blocker_id: UUID, blocked_id: UUID) -> Friend:
    """Block a user."""
    if blocker_id == blocked_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot block yourself"
        )
    
    # Find existing relationship
    existing = await Friend.find_one({
        "$or": [
            {"requester_id": blocker_id, "addressee_id": blocked_id},
            {"requester_id": blocked_id, "addressee_id": blocker_id}
        ]
    })
    
    if existing:
        existing.status = FriendRequestStatus.BLOCKED
        existing.updated_at = datetime.now()
        await existing.save()
        return existing
    
    # Create new block entry
    block = Friend(
        requester_id=blocker_id,
        addressee_id=blocked_id,
        status=FriendRequestStatus.BLOCKED
    )
    await block.insert()
    return block

