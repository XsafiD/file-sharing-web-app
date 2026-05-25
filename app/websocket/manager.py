"""
WebSocket Connection Manager
Manages real-time connections for file updates
"""

import asyncio
from typing import List, Set
from fastapi import WebSocket
from datetime import datetime
import json


class ConnectionManager:
    """
    Manages WebSocket connections for real-time updates
    Replaces polling with push-based updates
    """

    def __init__(self):
        # Store active connections
        self.active_connections: List[WebSocket] = []
        self._lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket) -> None:
        """
        Accept and register new WebSocket connection

        Args:
            websocket: WebSocket connection instance
        """
        await websocket.accept()
        async with self._lock:
            self.active_connections.append(websocket)

        # Send welcome message
        await websocket.send_json({
            'type': 'connected',
            'timestamp': datetime.now().isoformat(),
            'message': 'Connected to Webshare real-time updates'
        })

    async def disconnect(self, websocket: WebSocket) -> None:
        """
        Remove WebSocket connection

        Args:
            websocket: WebSocket connection to remove
        """
        async with self._lock:
            if websocket in self.active_connections:
                self.active_connections.remove(websocket)

    async def broadcast_files(self, files: list) -> None:
        """
        Broadcast file list updates to all connected clients

        Args:
            files: Updated file list to broadcast
        """
        if not self.active_connections:
            return

        message = {
            'type': 'files_update',
            'timestamp': datetime.now().isoformat(),
            'data': files
        }

        # Send to all connected clients
        disconnected = []
        async with self._lock:
            for connection in self.active_connections:
                try:
                    await connection.send_json(message)
                except Exception:
                    # Mark for removal
                    disconnected.append(connection)

        # Clean up disconnected clients
        for connection in disconnected:
            await self.disconnect(connection)

    async def broadcast_message(self, message_type: str, data: dict) -> None:
        """
        Broadcast custom message to all connected clients

        Args:
            message_type: Type of message
            data: Message data
        """
        if not self.active_connections:
            return

        message = {
            'type': message_type,
            'timestamp': datetime.now().isoformat(),
            'data': data
        }

        disconnected = []
        async with self._lock:
            for connection in self.active_connections:
                try:
                    await connection.send_json(message)
                except Exception:
                    disconnected.append(connection)

        for connection in disconnected:
            await self.disconnect(connection)

    async def get_connection_count(self) -> int:
        """Get current number of active connections"""
        async with self._lock:
            return len(self.active_connections)


# Global connection manager instance
_manager: ConnectionManager = None


def get_manager() -> ConnectionManager:
    """Get global connection manager instance"""
    global _manager
    if _manager is None:
        _manager = ConnectionManager()
    return _manager
