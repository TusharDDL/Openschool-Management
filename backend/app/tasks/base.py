from typing import Any, Dict, Optional
from celery import Task
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.core.redis import get_redis_client
from app.core.logger import get_logger

logger = get_logger(__name__)

class BaseTask(Task):
    _db: Optional[Session] = None

    @property
    def db(self) -> Session:
        if self._db is None:
            self._db = SessionLocal()
        return self._db

    def after_return(self, *args: Any, **kwargs: Any) -> None:
        if self._db is not None:
            self._db.close()
            self._db = None

    def on_failure(self, exc: Exception, task_id: str, args: Any, kwargs: Any, einfo: Any) -> None:
        logger.error(
            f"Task {self.name}[{task_id}] failed: {exc}",
            extra={
                "task_id": task_id,
                "args": args,
                "kwargs": kwargs,
                "exception": str(exc),
            },
        )

    def on_retry(self, exc: Exception, task_id: str, args: Any, kwargs: Any, einfo: Any) -> None:
        logger.warning(
            f"Task {self.name}[{task_id}] retrying: {exc}",
            extra={
                "task_id": task_id,
                "args": args,
                "kwargs": kwargs,
                "exception": str(exc),
            },
        )

    def on_success(self, retval: Any, task_id: str, args: Any, kwargs: Any) -> None:
        logger.info(
            f"Task {self.name}[{task_id}] completed successfully",
            extra={
                "task_id": task_id,
                "args": args,
                "kwargs": kwargs,
                "result": retval,
            },
        )

class DatabaseTask(BaseTask):
    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        try:
            return super().__call__(*args, **kwargs)
        finally:
            if self._db is not None:
                self._db.close()
                self._db = None

class CacheTask(BaseTask):
    _redis = None

    @property
    def redis(self):
        if self._redis is None:
            self._redis = get_redis_client()
        return self._redis

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        try:
            return super().__call__(*args, **kwargs)
        finally:
            if self._redis is not None:
                self._redis.close()
                self._redis = None