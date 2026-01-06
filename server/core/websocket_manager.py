"""WebSocket connection manager for real-time chat functionality."""
from typing import Dict, Set
from uuid import UUID
from fastapi import WebSocket
import logging

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Manages WebSocket connections for real-time messaging."""

    def __init__(self):
        # user_id -> set of websocket connections
        self._active_connections: Dict[UUID, Set[WebSocket]] = {}

    async def connect(self, user_id: UUID, websocket: WebSocket) -> None:
        """Connect a user's websocket."""
        await websocket.accept()
        
        if user_id not in self._active_connections:
            self._active_connections[user_id] = set()
        
        self._active_connections[user_id].add(websocket)
        logger.info(f"User {user_id} connected. Total connections: {len(self._active_connections[user_id])}")

    def disconnect(self, user_id: UUID, websocket: WebSocket) -> None:
        """Disconnect a user's websocket."""
        if user_id in self._active_connections:
            self._active_connections[user_id].discard(websocket)
            
            # Remove user entry if no more connections
            if not self._active_connections[user_id]:
                del self._active_connections[user_id]
                logger.info(f"User {user_id} fully disconnected")
            else:
                logger.info(f"User {user_id} disconnected one session. Remaining: {len(self._active_connections[user_id])}")

    async def send_personal_message(self, message: dict, user_id: UUID) -> None:
        """Send a message to a specific user (all their connections)."""
        if user_id in self._active_connections:
            disconnected = set()
            for connection in self._active_connections[user_id]:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    logger.error(f"Error sending message to user {user_id}: {e}")
                    disconnected.add(connection)
            
            # Clean up disconnected connections
            for conn in disconnected:
                self.disconnect(user_id, conn)

    async def broadcast_to_conversation(
        self, 
        message: dict, 
        conversation_id: UUID, 
        participant_ids: list[UUID],
        exclude_user_id: UUID | None = None
    ) -> None:
        """Broadcast a message to all participants in a conversation."""
        for participant_id in participant_ids:
            # Skip the sender if exclude_user_id is provided
            if exclude_user_id and participant_id == exclude_user_id:
                continue
            
            await self.send_personal_message(message, participant_id)

    def is_user_online(self, user_id: UUID) -> bool:
        """Check if a user has any active connections."""
        return user_id in self._active_connections and len(self._active_connections[user_id]) > 0

    def get_online_users(self) -> Set[UUID]:
        """Get set of all online user IDs."""
        return set(self._active_connections.keys())


# Global connection manager instance
connection_manager = ConnectionManager()

