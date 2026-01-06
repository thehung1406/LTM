"""Friend relationship model for user connections."""
from datetime import datetime
from uuid import UUID, uuid4
from enum import Enum
from beanie import Document
from pydantic import Field


class FriendRequestStatus(str, Enum):
    """Status of a friend request."""
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    BLOCKED = "blocked"


class Friend(Document):
    """Represents a friend relationship or friend request between two users."""
    
    id: UUID = Field(default_factory=uuid4, alias="_id")
    requester_id: UUID  # User who sent the friend request
    addressee_id: UUID  # User who received the friend request
    status: FriendRequestStatus = FriendRequestStatus.PENDING
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    class Settings:
        name = "friends"
        indexes = [
            "requester_id",
            "addressee_id",
            [("requester_id", 1), ("addressee_id", 1)],
        ]

