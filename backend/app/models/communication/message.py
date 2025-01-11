from enum import Enum
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum as SQLEnum, Text, JSON, UniqueConstraint
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class MessageType(str, Enum):
    ANNOUNCEMENT = "ANNOUNCEMENT"
    NOTICE = "NOTICE"
    HOMEWORK = "HOMEWORK"
    EVENT = "EVENT"
    REMINDER = "REMINDER"
    ALERT = "ALERT"
    OTHER = "OTHER"

class MessageStatus(str, Enum):
    DRAFT = "DRAFT"
    SCHEDULED = "SCHEDULED"
    SENT = "SENT"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"

class MessagePriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    URGENT = "URGENT"

class Message(BaseModel):
    __tablename__ = "messages"
    __table_args__ = {'schema': 'communication'}

    tenant_id = Column(Integer, ForeignKey("public.tenants.id", ondelete="CASCADE"), nullable=False)
    sender_id = Column(Integer, ForeignKey("public.users.id", ondelete="CASCADE"), nullable=False)
    
    message_type = Column(SQLEnum(MessageType), nullable=False)
    subject = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    priority = Column(SQLEnum(MessagePriority), nullable=False, default=MessagePriority.MEDIUM)
    status = Column(SQLEnum(MessageStatus), nullable=False, default=MessageStatus.DRAFT)
    scheduled_at = Column(DateTime)
    sent_at = Column(DateTime)
    metadata = Column(JSON)  # For additional message-specific data
    is_internal = Column(Boolean, default=False)  # For staff-only messages
    requires_acknowledgment = Column(Boolean, default=False)
    acknowledgment_deadline = Column(DateTime)

    # Relationships
    tenant = relationship("Tenant")
    sender = relationship("User", foreign_keys=[sender_id])
    recipients = relationship("MessageRecipient", back_populates="message", cascade="all, delete-orphan")
    attachments = relationship("MessageAttachment", back_populates="message", cascade="all, delete-orphan")

class MessageRecipient(BaseModel):
    __tablename__ = "message_recipients"
    __table_args__ = (
        UniqueConstraint('message_id', 'recipient_id', name='uq_message_recipient'),
        {'schema': 'communication'}
    )

    message_id = Column(Integer, ForeignKey("communication.messages.id", ondelete="CASCADE"), nullable=False)
    recipient_id = Column(Integer, ForeignKey("public.users.id", ondelete="CASCADE"), nullable=False)
    
    is_read = Column(Boolean, default=False)
    read_at = Column(DateTime)
    is_acknowledged = Column(Boolean, default=False)
    acknowledged_at = Column(DateTime)
    delivery_status = Column(String)  # For tracking email/SMS delivery
    error_message = Column(Text)

    # Relationships
    message = relationship("Message", back_populates="recipients")
    recipient = relationship("User")

class MessageAttachment(BaseModel):
    __tablename__ = "message_attachments"
    __table_args__ = {'schema': 'communication'}

    message_id = Column(Integer, ForeignKey("communication.messages.id", ondelete="CASCADE"), nullable=False)
    
    file_name = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)
    mime_type = Column(String, nullable=False)
    file_url = Column(String, nullable=False)
    is_public = Column(Boolean, default=True)

    # Relationships
    message = relationship("Message", back_populates="attachments")

class NotificationPreference(BaseModel):
    __tablename__ = "notification_preferences"
    __table_args__ = (
        UniqueConstraint('user_id', 'message_type', name='uq_notification_preference'),
        {'schema': 'communication'}
    )

    user_id = Column(Integer, ForeignKey("public.users.id", ondelete="CASCADE"), nullable=False)
    message_type = Column(SQLEnum(MessageType), nullable=False)
    
    email_enabled = Column(Boolean, default=True)
    sms_enabled = Column(Boolean, default=False)
    push_enabled = Column(Boolean, default=True)
    in_app_enabled = Column(Boolean, default=True)

    # Relationships
    user = relationship("User")

class NotificationTemplate(BaseModel):
    __tablename__ = "notification_templates"
    __table_args__ = (
        UniqueConstraint('tenant_id', 'code', name='uq_notification_template'),
        {'schema': 'communication'}
    )

    tenant_id = Column(Integer, ForeignKey("public.tenants.id", ondelete="CASCADE"), nullable=False)
    
    code = Column(String, nullable=False)  # Unique template identifier
    name = Column(String, nullable=False)
    description = Column(Text)
    message_type = Column(SQLEnum(MessageType), nullable=False)
    subject_template = Column(Text, nullable=False)
    content_template = Column(Text, nullable=False)
    metadata_schema = Column(JSON)  # JSON Schema for required variables
    is_active = Column(Boolean, default=True)

    # Relationships
    tenant = relationship("Tenant")