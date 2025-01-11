from typing import Any, Optional, List, Dict
from datetime import datetime
import json
import asyncio
from fastapi import WebSocket
from redis.asyncio import Redis
from app.core.config import get_settings

settings = get_settings()

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}
        self.redis: Optional[Redis] = None

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)

    async def disconnect(self, websocket: WebSocket, user_id: str):
        if user_id in self.active_connections:
            self.active_connections[user_id].remove(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]

    async def send_personal_message(self, message: str, user_id: str):
        if user_id in self.active_connections:
            for connection in self.active_connections[user_id]:
                try:
                    await connection.send_text(message)
                except Exception:
                    await self.disconnect(connection, user_id)

    async def broadcast(self, message: str, exclude_user: Optional[str] = None):
        for user_id, connections in self.active_connections.items():
            if user_id != exclude_user:
                for connection in connections:
                    try:
                        await connection.send_text(message)
                    except Exception:
                        await self.disconnect(connection, user_id)

    async def get_redis(self) -> Redis:
        if self.redis is None:
            self.redis = Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB,
                password=settings.REDIS_PASSWORD,
                decode_responses=True
            )
        return self.redis

class NotificationManager:
    def __init__(self, connection_manager: ConnectionManager):
        self.manager = connection_manager
        self.notification_channel = "notifications"

    async def start_listener(self):
        redis = await self.manager.get_redis()
        pubsub = redis.pubsub()
        await pubsub.subscribe(self.notification_channel)

        while True:
            try:
                message = await pubsub.get_message(ignore_subscribe_messages=True)
                if message and message["type"] == "message":
                    data = json.loads(message["data"])
                    await self.process_notification(data)
            except Exception as e:
                print(f"Notification listener error: {e}")
            await asyncio.sleep(0.1)

    async def process_notification(self, data: dict):
        notification_type = data.get("type")
        recipients = data.get("recipients", [])
        message = data.get("message")

        if notification_type == "personal":
            for recipient in recipients:
                await self.manager.send_personal_message(message, recipient)
        elif notification_type == "broadcast":
            exclude = data.get("exclude")
            await self.manager.broadcast(message, exclude)

    async def send_notification(self, notification_type: str, message: Any, recipients: List[str] = None, exclude: str = None):
        redis = await self.manager.get_redis()
        data = {
            "type": notification_type,
            "message": message,
            "recipients": recipients,
            "exclude": exclude,
            "timestamp": datetime.utcnow().isoformat()
        }
        await redis.publish(self.notification_channel, json.dumps(data))

    async def send_personal_notification(self, user_id: str, message: Any):
        await self.send_notification("personal", message, recipients=[user_id])

    async def send_broadcast_notification(self, message: Any, exclude_user: Optional[str] = None):
        await self.send_notification("broadcast", message, exclude=exclude_user)

# Create global instances
manager = ConnectionManager()
notifications = NotificationManager(manager)

# Start notification listener
@asyncio.create_task
async def start_notification_listener():
    await notifications.start_listener()