"""Schemas for friend-related operations."""
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel
from models.friend import FriendRequestStatus


class FriendRequestCreate(BaseModel):
    """Schema for creating a friend request."""
    addressee_id: UUID


class FriendRequestResponse(BaseModel):
    """Schema for friend request response."""
    id: UUID
    requester_id: UUID
    addressee_id: UUID
    status: FriendRequestStatus
    created_at: datetime
    updated_at: datetime


class FriendResponse(BaseModel):
    """Schema for friend response with user details."""
    id: UUID
    friend_id: UUID
    friend_username: str
    friend_fullname: str
    status: str
    last_online: datetime
    created_at: datetime

