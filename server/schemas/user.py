from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel

class UserCreate(BaseModel):
    fullname : str
    username: str
    password: str

class UserUpdate(BaseModel):
    """Schema for updating user profile (only allowed fields)."""
    fullname: Optional[str] = None

class PasswordChange(BaseModel):
    old_password: str
    new_password: str


class UserRead(BaseModel):
    id: UUID
    fullname: str
    username: str
    status: Optional[str] = None
    last_online: Optional[datetime] = None


class UserStats(BaseModel):
    """User statistics."""
    total_friends: int
    online_friends: int
    total_conversations: int
    unread_messages: int
