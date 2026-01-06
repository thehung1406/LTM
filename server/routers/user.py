"""User management endpoints."""
from typing import List
from fastapi import APIRouter, Query, Depends, status
from uuid import UUID

from models.user import User
from schemas.user import UserRead, UserUpdate, UserStats
from schemas.friend import FriendResponse
from services.user_service import (
    get_user_by_id,
    search_users,
    update_user_profile,
    get_user_statistics
)
from services.friend_service import get_friends_list
from utils.dependencies import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserRead)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current authenticated user's information."""
    return UserRead(**current_user.model_dump())


@router.patch("/me", response_model=UserRead)
async def update_my_profile(
    payload: UserUpdate,
    current_user: User = Depends(get_current_user)
):
    """Update current user's profile information."""
    user = await update_user_profile(current_user.id, payload)
    return UserRead(**user.model_dump())


@router.get("/me/stats", response_model=UserStats)
async def get_my_statistics(current_user: User = Depends(get_current_user)):
    """Get current user's statistics (friends count, unread messages, etc)."""
    stats = await get_user_statistics(current_user.id)
    return UserStats(**stats)


@router.get("/friends", response_model=List[FriendResponse])
async def get_my_friends(
    current_user: User = Depends(get_current_user)
):
    """Get list of friends (only users who are friends with current user)."""
    friends = await get_friends_list(current_user.id)
    return friends


@router.get("/friends/online", response_model=List[FriendResponse])
async def get_online_friends(
    current_user: User = Depends(get_current_user)
):
    """Get list of friends who are currently online."""
    all_friends = await get_friends_list(current_user.id)
    online_friends = [friend for friend in all_friends if friend.status == "online"]
    return online_friends


@router.get("/search", response_model=List[UserRead])
async def search_for_users(
    q: str = Query(..., min_length=1),
    limit: int = Query(10, ge=1, le=50),
    current_user: User = Depends(get_current_user)
):
    """Search users by username or fullname to send friend requests."""
    users = await search_users(q, limit)
    return users


@router.get("/{user_id}", response_model=UserRead)
async def get_user_by_id_endpoint(
    user_id: UUID,
    current_user: User = Depends(get_current_user)
):
    """Get a specific user's profile by their ID."""
    user = await get_user_by_id(str(user_id))
    return UserRead(**user.model_dump())

