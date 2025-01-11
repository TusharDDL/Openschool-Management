from enum import Enum
from sqlalchemy import Column, String, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class SaaSRole(str, Enum):
    SUPER_ADMIN = "SUPER_ADMIN"
    ADMIN = "ADMIN"
    SUPPORT = "SUPPORT"
    IMPLEMENTATION = "IMPLEMENTATION"

class SaaSAdmin(BaseModel):
    __tablename__ = "saas_admins"

    email = Column(String, unique=True, nullable=False, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    role = Column(SQLEnum(SaaSRole), nullable=False)
    is_active = Column(Boolean, default=True)
    full_name = Column(String)
    phone = Column(String)

    # Relationships
    assigned_tickets = relationship("SupportTicket", back_populates="assigned_to")
    assigned_tasks = relationship("OnboardingTask", back_populates="assigned_to")