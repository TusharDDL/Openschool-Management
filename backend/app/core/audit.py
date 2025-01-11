from typing import Optional, Dict, Any
from datetime import datetime
import json
from fastapi import Request, Response
from sqlalchemy.orm import Session
from app.models.audit import AuditLog, AuditAction, SessionActivity
from app.core.database import SessionLocal
from app.core.celery_app import celery_app

def get_client_info(request: Request) -> Dict[str, str]:
    """Extract client information from request"""
    return {
        "ip_address": request.client.host if request.client else None,
        "user_agent": request.headers.get("user-agent"),
        "referer": request.headers.get("referer"),
        "accept_language": request.headers.get("accept-language")
    }

def get_user_info(request: Request) -> Dict[str, Any]:
    """Extract user information from request state"""
    user = getattr(request.state, "user", None)
    return {
        "user_id": user.id if user else None,
        "tenant_id": user.tenant_id if user and hasattr(user, "tenant_id") else None,
        "role": user.role if user else None
    }

def get_request_body(request: Request) -> Optional[Dict]:
    """Safely extract request body"""
    try:
        return json.loads(request.body.decode())
    except:
        return None

@celery_app.task
def log_audit_async(
    action: str,
    entity_type: str,
    entity_id: Optional[str],
    user_id: Optional[int],
    tenant_id: Optional[int],
    old_values: Optional[Dict] = None,
    new_values: Optional[Dict] = None,
    client_info: Optional[Dict] = None,
    request_info: Optional[Dict] = None,
    response_info: Optional[Dict] = None,
    metadata: Optional[Dict] = None
):
    """Asynchronously create audit log entry"""
    with SessionLocal() as db:
        log = AuditLog(
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            user_id=user_id,
            tenant_id=tenant_id,
            old_values=old_values,
            new_values=new_values,
            ip_address=client_info.get("ip_address") if client_info else None,
            user_agent=client_info.get("user_agent") if client_info else None,
            endpoint=request_info.get("endpoint") if request_info else None,
            request_method=request_info.get("method") if request_info else None,
            request_body=request_info.get("body") if request_info else None,
            response_status=response_info.get("status") if response_info else None,
            error_message=response_info.get("error") if response_info else None,
            metadata=metadata
        )
        db.add(log)
        db.commit()

@celery_app.task
def log_session_activity_async(
    session_id: str,
    endpoint: str,
    method: str,
    status_code: int,
    response_time: float,
    ip_address: str,
    metadata: Optional[Dict] = None
):
    """Asynchronously log session activity"""
    with SessionLocal() as db:
        activity = SessionActivity(
            session_id=session_id,
            endpoint=endpoint,
            method=method,
            status_code=status_code,
            response_time=response_time,
            ip_address=ip_address,
            metadata=metadata
        )
        db.add(activity)
        db.commit()

class AuditLogger:
    def __init__(self, db: Session):
        self.db = db

    def log_data_change(
        self,
        table_name: str,
        record_id: str,
        operation: str,
        old_data: Optional[Dict] = None,
        new_data: Optional[Dict] = None,
        user_id: Optional[int] = None,
        tenant_id: Optional[int] = None,
        change_reason: Optional[str] = None,
        requires_approval: bool = False
    ):
        """Log data changes that require approval"""
        log = DataChangeLog(
            table_name=table_name,
            record_id=record_id,
            operation=operation,
            old_data=old_data,
            new_data=new_data,
            changed_by_id=user_id,
            tenant_id=tenant_id,
            change_reason=change_reason,
            requires_approval=requires_approval,
            is_system_change=user_id is None
        )
        self.db.add(log)
        self.db.commit()
        return log

    def approve_change(
        self,
        change_id: int,
        approved_by_id: int,
        approval_notes: Optional[str] = None
    ):
        """Approve a data change"""
        change = self.db.query(DataChangeLog).filter_by(id=change_id).first()
        if change:
            change.is_approved = True
            change.approved_by_id = approved_by_id
            change.approval_date = datetime.utcnow()
            change.approval_notes = approval_notes
            self.db.commit()
        return change

def audit_request(
    request: Request,
    response: Response,
    action: AuditAction,
    entity_type: str,
    entity_id: Optional[str] = None,
    old_values: Optional[Dict] = None,
    new_values: Optional[Dict] = None,
    metadata: Optional[Dict] = None
):
    """Audit a request with all context"""
    client_info = get_client_info(request)
    user_info = get_user_info(request)
    
    request_info = {
        "endpoint": str(request.url),
        "method": request.method,
        "body": get_request_body(request)
    }
    
    response_info = {
        "status": response.status_code,
        "error": None
    }
    if response.status_code >= 400 and hasattr(response, 'body'):
        try:
            response_info["error"] = str(response.body)
        except:
            pass

    # Log asynchronously
    log_audit_async.delay(
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        user_id=user_info.get("user_id"),
        tenant_id=user_info.get("tenant_id"),
        old_values=old_values,
        new_values=new_values,
        client_info=client_info,
        request_info=request_info,
        response_info=response_info,
        metadata=metadata
    )