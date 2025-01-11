from enum import Enum
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum as SQLEnum, Text, DateTime
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class TicketStatus(str, Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    ESCALATED = "ESCALATED"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"

class TicketPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class SupportTicket(BaseModel):
    __tablename__ = "support_tickets"

    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    status = Column(SQLEnum(TicketStatus), nullable=False, default=TicketStatus.OPEN)
    priority = Column(SQLEnum(TicketPriority), nullable=False, default=TicketPriority.MEDIUM)
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False)
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    assigned_to_id = Column(Integer, ForeignKey("saas_admins.id"))
    resolved_at = Column(DateTime)
    resolution_notes = Column(Text)

    # Relationships
    school = relationship("School", backref="support_tickets")
    created_by = relationship("User", back_populates="created_tickets")
    assigned_to = relationship("SaaSAdmin", back_populates="assigned_tickets")
    comments = relationship("TicketComment", back_populates="ticket")

class TicketComment(BaseModel):
    __tablename__ = "ticket_comments"

    ticket_id = Column(Integer, ForeignKey("support_tickets.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    is_internal = Column(Boolean, default=False)  # For internal team notes

    # Relationships
    ticket = relationship("SupportTicket", back_populates="comments")
    user = relationship("User", back_populates="ticket_comments")