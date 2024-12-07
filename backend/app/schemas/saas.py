from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from app.models.saas import SaaSRole, TicketStatus, TicketPriority, OnboardingTaskStatus

# SaaS Admin Schemas
class SaaSAdminBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3)
    full_name: Optional[str] = None
    phone: Optional[str] = None
    role: SaaSRole
    is_active: bool = True

class SaaSAdminCreate(SaaSAdminBase):
    password: str = Field(..., min_length=8)

class SaaSAdminUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    phone: Optional[str] = None
    role: Optional[SaaSRole] = None
    is_active: Optional[bool] = None
    password: Optional[str] = Field(None, min_length=8)

class SaaSAdminResponse(SaaSAdminBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Support Ticket Schemas
class SupportTicketBase(BaseModel):
    title: str = Field(..., min_length=5)
    description: str = Field(..., min_length=10)
    priority: TicketPriority
    school_id: int
    assigned_to_id: Optional[int] = None

class SupportTicketCreate(SupportTicketBase):
    pass

class SupportTicketUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=5)
    description: Optional[str] = Field(None, min_length=10)
    status: Optional[TicketStatus] = None
    priority: Optional[TicketPriority] = None
    assigned_to_id: Optional[int] = None
    resolution_notes: Optional[str] = None

class SupportTicketResponse(SupportTicketBase):
    id: int
    status: TicketStatus
    created_by_id: int
    resolved_at: Optional[datetime]
    resolution_notes: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Ticket Comment Schemas
class TicketCommentBase(BaseModel):
    content: str = Field(..., min_length=1)
    is_internal: bool = False

class TicketCommentCreate(TicketCommentBase):
    pass

class TicketCommentResponse(TicketCommentBase):
    id: int
    ticket_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Onboarding Task Schemas
class OnboardingTaskBase(BaseModel):
    school_id: int
    title: str = Field(..., min_length=5)
    description: Optional[str] = None
    assigned_to_id: Optional[int] = None
    due_date: Optional[datetime] = None
    order: int
    is_blocking: bool = False

class OnboardingTaskCreate(OnboardingTaskBase):
    dependencies: Optional[List[int]] = None  # List of task IDs this task depends on

class OnboardingTaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=5)
    description: Optional[str] = None
    status: Optional[OnboardingTaskStatus] = None
    assigned_to_id: Optional[int] = None
    due_date: Optional[datetime] = None
    completion_notes: Optional[str] = None
    order: Optional[int] = None
    is_blocking: Optional[bool] = None
    dependencies: Optional[List[int]] = None

class OnboardingTaskResponse(OnboardingTaskBase):
    id: int
    status: OnboardingTaskStatus
    completed_at: Optional[datetime]
    completion_notes: Optional[str]
    created_at: datetime
    updated_at: datetime
    dependencies: List[int]  # List of task IDs this task depends on

    class Config:
        orm_mode = True