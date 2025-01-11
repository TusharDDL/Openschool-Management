from celery import Celery
from app.core.config import get_settings

settings = get_settings()

celery_app = Celery(
    "school_management",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=[
        "app.tasks.notifications",
        "app.tasks.reports",
        "app.tasks.academic",
        "app.tasks.system"
    ]
)

# Configure Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=3600,  # 1 hour
    worker_max_tasks_per_child=1000,
    broker_connection_retry_on_startup=True,
)

# Optional configuration for task routing
celery_app.conf.task_routes = {
    "app.tasks.notifications.*": {"queue": "notifications"},
    "app.tasks.reports.*": {"queue": "reports"},
    "app.tasks.academic.*": {"queue": "academic"},
    "app.tasks.system.*": {"queue": "system"},
}

# Optional configuration for task schedules
celery_app.conf.beat_schedule = {
    "cleanup-old-notifications": {
        "task": "app.tasks.system.cleanup_old_notifications",
        "schedule": 86400.0,  # Daily
    },
    "generate-daily-reports": {
        "task": "app.tasks.reports.generate_daily_reports",
        "schedule": 3600.0,  # Hourly
    },
    "sync-attendance": {
        "task": "app.tasks.academic.sync_attendance",
        "schedule": 300.0,  # Every 5 minutes
    },
}