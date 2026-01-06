"""Main FastAPI application for real-time chat server."""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from core.database import init_db, close
from routers import auth, user, chat, friend, ws

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager for startup and shutdown events."""
    # Startup
    await init_db()
    logger.info("✅ Database connected successfully!")
    yield
    # Shutdown
    await close()
    logger.info("🔌 Database connection closed")


# Initialize FastAPI application
app = FastAPI(
    title="Chat App API",
    description="Real-time chat application with WebSocket support",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Middleware Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include all routers
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(chat.router)
app.include_router(friend.router)
app.include_router(ws.router)
