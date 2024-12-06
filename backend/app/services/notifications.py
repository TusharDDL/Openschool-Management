from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.core.redis import get_redis_client
from app.models.user import User
from app.tasks.email import send_email
from app.core.config import settings

class Notification(BaseModel):
    id: str
    user_id: str
    title: str
    message: str
    type: str
    read: bool = False
    data: Optional[Dict[str, Any]] = None
    created_at: datetime

class NotificationService:
    def __init__(self, db: Session):
        self.db = db
        self.redis = get_redis_client()

    async def send_notification(
        self,
        user_id: str,
        title: str,
        message: str,
        notification_type: str,
        data: Optional[Dict[str, Any]] = None,
        send_email: bool = False
    ) -> Notification:
        """Send notification to user"""
        notification = Notification(
            id=str(uuid.uuid4()),
            user_id=user_id,
            title=title,
            message=message,
            type=notification_type,
            data=data,
            created_at=datetime.utcnow()
        )

        # Store in Redis
        key = f"notifications:{user_id}"
        self.redis.lpush(key, notification.json())
        self.redis.ltrim(key, 0, 99)  # Keep last 100 notifications

        # Send email if requested
        if send_email:
            user = self.db.query(User).filter(User.id == user_id).first()
            if user and user.email:
                send_email.delay(
                    to_email=user.email,
                    subject=title,
                    template_name="notification",
                    context={
                        "title": title,
                        "message": message,
                        "name": user.full_name
                    }
                )

        # Emit WebSocket event
        await self._emit_notification(user_id, notification)

        return notification

    async def get_notifications(
        self,
        user_id: str,
        page: int = 1,
        per_page: int = 20
    ) -> List[Notification]:
        """Get user notifications"""
        key = f"notifications:{user_id}"
        start = (page - 1) * per_page
        end = start + per_page - 1

        notifications = self.redis.lrange(key, start, end)
        return [Notification.parse_raw(n) for n in notifications]

    async def mark_as_read(
        self,
        user_id: str,
        notification_id: str
    ) -> bool:
        """Mark notification as read"""
        key = f"notifications:{user_id}"
        notifications = self.redis.lrange(key, 0, -1)
        
        for i, n_data in enumerate(notifications):
            notification = Notification.parse_raw(n_data)
            if notification.id == notification_id:
                notification.read = True
                self.redis.lset(key, i, notification.json())
                return True
        
        return False

    async def mark_all_as_read(self, user_id: str) -> int:
        """Mark all notifications as read"""
        key = f"notifications:{user_id}"
        notifications = self.redis.lrange(key, 0, -1)
        count = 0

        for i, n_data in enumerate(notifications):
            notification = Notification.parse_raw(n_data)
            if not notification.read:
                notification.read = True
                self.redis.lset(key, i, notification.json())
                count += 1

        return count

    async def delete_notification(
        self,
        user_id: str,
        notification_id: str
    ) -> bool:
        """Delete notification"""
        key = f"notifications:{user_id}"
        notifications = self.redis.lrange(key, 0, -1)
        
        for n_data in notifications:
            notification = Notification.parse_raw(n_data)
            if notification.id == notification_id:
                self.redis.lrem(key, 1, n_data)
                return True
        
        return False

    async def get_unread_count(self, user_id: str) -> int:
        """Get count of unread notifications"""
        key = f"notifications:{user_id}"
        notifications = self.redis.lrange(key, 0, -1)
        return sum(
            1 for n in notifications
            if not Notification.parse_raw(n).read
        )

    async def _emit_notification(
        self,
        user_id: str,
        notification: Notification
    ) -> None:
        """Emit WebSocket event for real-time notifications"""
        # This is a placeholder for WebSocket implementation
        # You'll need to implement the actual WebSocket logic
        pass

    @staticmethod
    async def send_bulk_notification(
        db: Session,
        user_ids: List[str],
        title: str,
        message: str,
        notification_type: str,
        data: Optional[Dict[str, Any]] = None,
        send_email: bool = False
    ) -> int:
        """Send notification to multiple users"""
        service = NotificationService(db)
        count = 0

        for user_id in user_ids:
            try:
                await service.send_notification(
                    user_id=user_id,
                    title=title,
                    message=message,
                    notification_type=notification_type,
                    data=data,
                    send_email=send_email
                )
                count += 1
            except Exception as e:
                logger.error(
                    f"Failed to send notification to user {user_id}: {str(e)}"
                )

        return count

# Notification Types
class NotificationType:
    SYSTEM = "system"
    ASSIGNMENT = "assignment"
    GRADE = "grade"
    ATTENDANCE = "attendance"
    ANNOUNCEMENT = "announcement"
    MESSAGE = "message"