from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional
from schemas.message import MessageResponse


class ConversationCreate(BaseModel):
    """Create conversation with another user."""
    participant_id: UUID


class ParticipantInfo(BaseModel):
    """Participant information in conversation."""
    id: UUID
    username: str
    fullname: str
    status: str
    last_online: datetime


class ConversationResponse(BaseModel):
    """Conversation list response with participant details."""
    id: UUID
    participants: list[ParticipantInfo]  # Full user info instead of just UUIDs
    created_at: datetime
    last_message_at: datetime
    last_message: Optional[str] = None
    unread_count: int = 0


class ConversationDetailResponse(BaseModel):
    """Detailed conversation with messages and participant info."""
    id: UUID
    participants: list[ParticipantInfo]
    created_at: datetime
    messages: list[MessageResponse]
    total_messages: int