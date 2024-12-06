from typing import Dict, Set
from fastapi import WebSocket, WebSocketDisconnect
from app.core.logger import get_logger

logger = get_logger(__name__)

class ConnectionManager:
    def __init__(self):
        # Map user_id to set of WebSocket connections
        self.active_connections: Dict[str, Set[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = set()
        self.active_connections[user_id].add(websocket)
        logger.info(f"WebSocket connection established for user {user_id}")

    def disconnect(self, websocket: WebSocket, user_id: str):
        if user_id in self.active_connections:
            self.active_connections[user_id].discard(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]
        logger.info(f"WebSocket connection closed for user {user_id}")

    async def send_personal_message(self, message: dict, user_id: str):
        if user_id in self.active_connections:
            disconnected = set()
            for connection in self.active_connections[user_id]:
                try:
                    await connection.send_json(message)
                except WebSocketDisconnect:
                    disconnected.add(connection)
                except Exception as e:
                    logger.error(f"Error sending message to user {user_id}: {str(e)}")
                    disconnected.add(connection)
            
            # Clean up disconnected connections
            for connection in disconnected:
                self.active_connections[user_id].discard(connection)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]

    async def broadcast(self, message: dict, exclude_user: str = None):
        disconnected_users = set()
        for user_id, connections in self.active_connections.items():
            if user_id != exclude_user:
                disconnected = set()
                for connection in connections:
                    try:
                        await connection.send_json(message)
                    except WebSocketDisconnect:
                        disconnected.add(connection)
                    except Exception as e:
                        logger.error(f"Error broadcasting to user {user_id}: {str(e)}")
                        disconnected.add(connection)
                
                # Clean up disconnected connections
                for connection in disconnected:
                    connections.discard(connection)
                if not connections:
                    disconnected_users.add(user_id)
        
        # Clean up users with no connections
        for user_id in disconnected_users:
            del self.active_connections[user_id]

manager = ConnectionManager()

async def get_websocket_manager() -> ConnectionManager:
    return manager