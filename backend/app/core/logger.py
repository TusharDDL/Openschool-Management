import logging
import json
import sys
from datetime import datetime
from typing import Any, Dict
from pathlib import Path
from logging.handlers import RotatingFileHandler
from app.core.config import settings

class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_obj: Dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        if hasattr(record, "request_id"):
            log_obj["request_id"] = record.request_id

        if record.exc_info:
            log_obj["exception"] = self.formatException(record.exc_info)

        if hasattr(record, "extra"):
            log_obj["extra"] = record.extra

        return json.dumps(log_obj)

def setup_logging() -> None:
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(settings.LOG_LEVEL)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(JSONFormatter())
    root_logger.addHandler(console_handler)

    # File handler
    file_handler = RotatingFileHandler(
        filename=log_dir / "app.log",
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setFormatter(JSONFormatter())
    root_logger.addHandler(file_handler)

    # Set levels for third-party loggers
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy").setLevel(logging.WARNING)
    logging.getLogger("celery").setLevel(logging.WARNING)

def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)

class LoggerMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        # Generate request ID
        request_id = scope.get("headers", {}).get(b"x-request-id", str(uuid.uuid4()))
        
        # Add request ID to logging context
        logger = logging.LoggerAdapter(
            get_logger(__name__),
            {"request_id": request_id}
        )

        # Log request
        logger.info(
            f"Request: {scope['method']} {scope['path']}",
            extra={
                "method": scope["method"],
                "path": scope["path"],
                "query_string": scope["query_string"],
                "client": scope["client"],
            },
        )

        # Process request
        start_time = time.time()
        try:
            response = await self.app(scope, receive, send)
            duration = time.time() - start_time
            
            # Log response
            logger.info(
                f"Response: {response['status']}",
                extra={
                    "status": response["status"],
                    "duration": duration,
                },
            )
            
            return response
        except Exception as e:
            duration = time.time() - start_time
            logger.error(
                f"Error processing request: {str(e)}",
                extra={
                    "duration": duration,
                    "error": str(e),
                },
                exc_info=True,
            )
            raise