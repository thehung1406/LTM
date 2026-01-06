from beanie import Document
from pydantic import Field
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional

class Message(Document):
    id: UUID = Field(default_factory=uuid4, alias="_id")
    conversation_id: UUID
    sender_id: UUID
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)
    is_read: bool = False
    read_at: Optional[datetime] = None