from celery import Celery
from celery.schedules import crontab
from typing import List, Dict, Any
import pandas as pd
from app.core.config import settings
from app.core.database import SessionLocal
from app.core.cache import CacheService
from app.services.notifications import NotificationService
from app.services.reports import ReportGenerator

celery = Celery(
    "school_management",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

celery.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=3600,  # 1 hour
    task_soft_time_limit=3300,  # 55 minutes
    worker_max_tasks_per_child=200,
    worker_prefetch_multiplier=1
)

# Configure scheduled tasks
celery.conf.beat_schedule = {
    "cleanup-expired-files": {
        "task": "app.worker.cleanup_expired_files",
        "schedule": crontab(hour=2, minute=0)  # Run at 2 AM daily
    },
    "generate-daily-reports": {
        "task": "app.worker.generate_daily_reports",
        "schedule": crontab(hour=1, minute=0)  # Run at 1 AM daily
    }
}

@celery.task(bind=True, max_retries=3)
def send_bulk_notifications(self, school_id: int, user_ids: List[int], message: Dict[str, Any]):
    try:
        notification_service = NotificationService()
        with SessionLocal() as db:
            for user_id in user_ids:
                try:
                    notification_service.send(db, user_id, message)
                except Exception as e:
                    # Log error but continue with other users
                    print(f"Error sending notification to user {user_id}: {str(e)}")
    except Exception as exc:
        self.retry(exc=exc, countdown=60)  # Retry after 1 minute

@celery.task(bind=True, max_retries=3)
def generate_report(
    self,
    school_id: int,
    report_type: str,
    filters: Dict[str, Any],
    user_id: int
):
    try:
        report_gen = ReportGenerator()
        with SessionLocal() as db:
            # Generate report
            report_data = report_gen.generate(db, school_id, report_type, filters)
            
            # Convert to Excel if needed
            if filters.get("format") == "excel":
                df = pd.DataFrame(report_data)
                excel_file = f"/tmp/report_{school_id}_{report_type}.xlsx"
                df.to_excel(excel_file, index=False)
                report_data = {"file_path": excel_file}
            
            # Cache the result
            cache = CacheService()
            cache_key = f"report:{school_id}:{report_type}:{user_id}"
            cache.set(cache_key, report_data, ttl=3600)  # Cache for 1 hour
            
            return {"status": "completed", "cache_key": cache_key}
    except Exception as exc:
        self.retry(exc=exc, countdown=60)

@celery.task
def cleanup_expired_files():
    """Daily cleanup of expired temporary files"""
    import os
    from datetime import datetime, timedelta
    
    tmp_dir = "/tmp"
    expiry_hours = 24
    
    now = datetime.now()
    for filename in os.listdir(tmp_dir):
        if filename.startswith("report_"):
            filepath = os.path.join(tmp_dir, filename)
            file_modified = datetime.fromtimestamp(os.path.getmtime(filepath))
            if now - file_modified > timedelta(hours=expiry_hours):
                os.remove(filepath)

@celery.task
def generate_daily_reports():
    """Generate daily summary reports for all schools"""
    with SessionLocal() as db:
        schools = db.query(School).filter(School.is_active == True).all()
        for school in schools:
            generate_report.delay(
                school_id=school.id,
                report_type="daily_summary",
                filters={"date": datetime.now().date().isoformat()},
                user_id=school.admin_id
            )

# Error handling and monitoring
@celery.task
def error_handler(request, exc, traceback, delivery_info):
    """Handle failed tasks"""
    task_id = request.id
    task_name = request.task
    
    # Log error details
    error_details = {
        "task_id": task_id,
        "task_name": task_name,
        "error": str(exc),
        "traceback": traceback,
        "delivery_info": delivery_info
    }
    print(f"Task failed: {error_details}")  # Replace with proper logging
    
    # Notify admins for critical errors
    if isinstance(exc, (MemoryError, TimeoutError)):
        send_bulk_notifications.delay(
            school_id=0,  # System notifications
            user_ids=[1],  # Admin user IDs
            message={
                "type": "error",
                "title": "Critical Task Error",
                "body": f"Task {task_name} failed: {str(exc)}"
            }
        )