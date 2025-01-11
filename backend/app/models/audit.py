from enum import Enum
from sqlalchemy import Column, Integer, String, JSON, ForeignKey, Enum as SQLEnum, Text, Boolean, DateTime, Float
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class AuditAction(str, Enum):
    CREATE = "CREATE"
    READ = "READ"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    LOGIN = "LOGIN"
    LOGOUT = "LOGOUT"
    EXPORT = "EXPORT"
    IMPORT = "IMPORT"
    APPROVE = "APPROVE"
    REJECT = "REJECT"
    OTHER = "OTHER"

class AuditLog(BaseModel):
    __tablename__ = "audit_logs"
    #__table_args__ = {'schema': 'system'}

    tenant_id = Column(Integer, ForeignKey("tenants.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    
    action = Column(SQLEnum(AuditAction), nullable=False)
    entity_type = Column(String, nullable=False)  # e.g., "student", "class", "exam"
    entity_id = Column(String)  # Primary key of the affected entity
    old_values = Column(JSON)  # Previous state for updates
    new_values = Column(JSON)  # New state for creates/updates
    ip_address = Column(String)
    user_agent = Column(String)
    endpoint = Column(String)  # API endpoint
    request_method = Column(String)  # HTTP method
    request_body = Column(JSON)  # Request payload
    response_status = Column(Integer)  # HTTP status code
    error_message = Column(Text)
    meta_data = Column(JSON)  # Additional context

    # Relationships
    tenant = relationship("Tenant")
    user = relationship("User")

class DataChangeLog(BaseModel):
    __tablename__ = "data_change_logs"
    #__table_args__ = {'schema': 'system'}

    tenant_id = Column(Integer, ForeignKey("tenants.id", ondelete="CASCADE"))
    changed_by_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    approved_by_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    
    table_name = Column(String, nullable=False)
    record_id = Column(String, nullable=False)
    operation = Column(String, nullable=False)  # INSERT, UPDATE, DELETE
    old_data = Column(JSON)
    new_data = Column(JSON)
    change_reason = Column(Text)
    requires_approval = Column(Boolean, default=False)
    is_approved = Column(Boolean)
    approval_date = Column(DateTime)
    approval_notes = Column(Text)
    is_system_change = Column(Boolean, default=False)

    # Relationships
    tenant = relationship("Tenant")
    changed_by = relationship("User", foreign_keys=[changed_by_id])
    approved_by = relationship("User", foreign_keys=[approved_by_id])

class LoginAttempt(BaseModel):
    __tablename__ = "login_attempts"
    #__table_args__ = {'schema': 'system'}

    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    
    email = Column(String, nullable=False)
    ip_address = Column(String, nullable=False)
    user_agent = Column(String)
    is_successful = Column(Boolean, nullable=False)
    failure_reason = Column(String)
    location = Column(String)  # Geo-location based on IP
    device_info = Column(JSON)  # Parsed user agent info

    # Relationships
    user = relationship("User")

class UserSession(BaseModel):
    __tablename__ = "user_sessions"
    #__table_args__ = {'schema': 'system'}

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    session_id = Column(String, nullable=False, unique=True)
    ip_address = Column(String, nullable=False)
    user_agent = Column(String)
    device_info = Column(JSON)
    location = Column(String)
    last_activity = Column(DateTime)
    expires_at = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)
    logout_time = Column(DateTime)
    logout_reason = Column(String)

    # Relationships
    user = relationship("User")
    activities = relationship("SessionActivity", back_populates="session", cascade="all, delete-orphan", primaryjoin="UserSession.session_id==SessionActivity.session_id")

class SessionActivity(BaseModel):
    __tablename__ = "session_activities"
    #__table_args__ = {'schema': 'system'}

    session_id = Column(String, ForeignKey("user_sessions.session_id", ondelete="CASCADE"), nullable=False)
    
    endpoint = Column(String, nullable=False)
    method = Column(String, nullable=False)
    status_code = Column(Integer)
    response_time = Column(Float)  # in milliseconds
    ip_address = Column(String)
    meta_data = Column(JSON)

    # Relationships
    session = relationship("UserSession", back_populates="activities")