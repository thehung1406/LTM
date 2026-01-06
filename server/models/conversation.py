from beanie import Document
from pydantic import Field
from uuid import UUID, uuid4
from datetime import datetime
from typing import List, Optional

class Conversation(Document):
    id: UUID = Field(default_factory=uuid4, alias="_id")
    participants: List[UUID] # list các user
    created_at: datetime = Field(default_factory=datetime.now)
    last_message_at: datetime = Field(default_factory=datetime.now)
    last_message: Optional[str] = None
