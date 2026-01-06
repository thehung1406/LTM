"""Database configuration and initialization."""
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
import certifi

from core.config import settings
from models.conversation import Conversation
from models.message import Message
from models.user import User
from models.friend import Friend

# Initialize MongoDB client
client = AsyncIOMotorClient(settings.MONGODB_URI, tlsCAFile=certifi.where())
db = client[settings.DATABASE_NAME]

# Collection references (for direct access if needed)
users_collection = db["User"]
messages_collection = db["Message"]
conversations_collection = db["Conversation"]
friends_collection = db["friends"]


async def init_db() -> None:
    """Initialize database and Beanie ODM with all document models."""
    await init_beanie(
        database=db,
        document_models=[User, Message, Conversation, Friend]
    )


async def close() -> None:
    """Close database connection."""
    client.close()