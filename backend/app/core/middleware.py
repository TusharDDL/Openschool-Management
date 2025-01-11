from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import time
from typing import Callable
import logging
from app.core.audit import audit_request, log_session_activity_async, AuditAction

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        
        # Process the request
        response = await call_next(request)
        
        # Calculate processing time
        process_time = time.time() - start_time
        
        # Log request info
        logger.info(
            f"Path: {request.url.path} "
            f"Method: {request.method} "
            f"Status: {response.status_code} "
            f"Duration: {process_time:.3f}s"
        )

        # Log session activity if user is authenticated
        user = getattr(request.state, "user", None)
        if user and hasattr(request.state, "session_id"):
            log_session_activity_async.delay(
                session_id=request.state.session_id,
                endpoint=str(request.url),
                method=request.method,
                status_code=response.status_code,
                response_time=process_time * 1000,  # Convert to milliseconds
                ip_address=request.client.host if request.client else None,
                metadata={
                    "user_id": user.id,
                    "tenant_id": getattr(user, "tenant_id", None),
                    "role": user.role
                }
            )

        # Audit sensitive operations
        if request.method in ["POST", "PUT", "DELETE", "PATCH"]:
            path = request.url.path.lower()
            
            # Map paths to entity types
            entity_mappings = {
                "/api/v1/users": "user",
                "/api/v1/schools": "school",
                "/api/v1/students": "student",
                "/api/v1/teachers": "teacher",
                "/api/v1/classes": "class",
                "/api/v1/subjects": "subject",
                "/api/v1/exams": "exam",
                "/api/v1/assignments": "assignment",
                "/api/v1/timetables": "timetable",
                "/api/v1/fees": "fee",
                "/api/v1/payments": "payment",
                "/api/v1/attendance": "attendance",
                "/api/v1/grades": "grade",
                "/api/v1/reports": "report",
                "/api/v1/settings": "setting"
            }

            # Find matching entity type
            entity_type = None
            for path_prefix, etype in entity_mappings.items():
                if path.startswith(path_prefix):
                    entity_type = etype
                    break

            if entity_type:
                # Map HTTP methods to audit actions
                action_mapping = {
                    "POST": AuditAction.CREATE,
                    "PUT": AuditAction.UPDATE,
                    "PATCH": AuditAction.UPDATE,
                    "DELETE": AuditAction.DELETE
                }

                # Extract entity ID from path for updates and deletes
                entity_id = None
                if request.method != "POST":
                    parts = path.split("/")
                    if len(parts) > 4 and parts[4].isdigit():
                        entity_id = parts[4]

                audit_request(
                    request=request,
                    response=response,
                    action=action_mapping[request.method],
                    entity_type=entity_type,
                    entity_id=entity_id
                )
        
        return response

class RequestValidationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        if request.method in ["POST", "PUT", "PATCH"]:
            content_type = request.headers.get("content-type", "")
            if not content_type.startswith("application/json"):
                return Response(
                    content="Content-Type must be application/json",
                    status_code=400
                )
        
        response = await call_next(request)
        return response