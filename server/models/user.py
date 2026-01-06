from datetime import datetime
from uuid import uuid4, UUID
from pydantic import  Field
from beanie import Document

class User(Document):
    id: UUID = Field(default_factory=uuid4, alias="_id")
    fullname: str
    username: str
    hashed_password: str
    status: str = "offline"
    last_online: datetime = Field(default_factory=datetime.now)

