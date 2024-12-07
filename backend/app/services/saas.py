from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from fastapi import HTTPException, status
from app.core.security import get_password_hash
from app.models.saas import (
    SaaSAdmin, SupportTicket, TicketComment, OnboardingTask,
    TicketStatus, OnboardingTaskStatus
)
from app.schemas.saas import (
    SaaSAdminCreate, SaaSAdminUpdate,
    SupportTicketCreate, SupportTicketUpdate,
    OnboardingTaskCreate, OnboardingTaskUpdate,
    TicketCommentCreate
)

# SaaS Admin Services
async def create_saas_admin(db: Session, data: SaaSAdminCreate) -> SaaSAdmin:
    # Check if email or username already exists
    existing_admin = db.query(SaaSAdmin).filter(
        or_(
            SaaSAdmin.email == data.email,
            SaaSAdmin.username == data.username
        )
    ).first()
    if existing_admin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email or username already registered"
        )

    # Create new admin
    admin = SaaSAdmin(
        **data.dict(exclude={"password"}),
        hashed_password=get_password_hash(data.password)
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin

async def get_saas_admin(db: Session, admin_id: int) -> Optional[SaaSAdmin]:
    return db.query(SaaSAdmin).filter(SaaSAdmin.id == admin_id).first()

async def get_saas_admins(
    db: Session,
    role: Optional[str] = None,
    is_active: Optional[bool] = None,
    skip: int = 0,
    limit: int = 100
) -> List[SaaSAdmin]:
    query = db.query(SaaSAdmin)
    if role:
        query = query.filter(SaaSAdmin.role == role)
    if is_active is not None:
        query = query.filter(SaaSAdmin.is_active == is_active)
    return query.offset(skip).limit(limit).all()

async def update_saas_admin(
    db: Session,
    admin_id: int,
    data: SaaSAdminUpdate
) -> Optional[SaaSAdmin]:
    admin = await get_saas_admin(db, admin_id)
    if not admin:
        return None

    # Update fields
    update_data = data.dict(exclude_unset=True)
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))

    for field, value in update_data.items():
        setattr(admin, field, value)

    db.commit()
    db.refresh(admin)
    return admin

# Support Ticket Services
async def create_support_ticket(
    db: Session,
    data: SupportTicketCreate,
    created_by_id: int
) -> SupportTicket:
    ticket = SupportTicket(
        **data.dict(),
        created_by_id=created_by_id,
        status=TicketStatus.OPEN
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket

async def get_support_ticket(db: Session, ticket_id: int) -> Optional[SupportTicket]:
    return db.query(SupportTicket).filter(SupportTicket.id == ticket_id).first()

async def get_support_tickets(
    db: Session,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    school_id: Optional[int] = None,
    assigned_to_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100
) -> List[SupportTicket]:
    query = db.query(SupportTicket)
    if status:
        query = query.filter(SupportTicket.status == status)
    if priority:
        query = query.filter(SupportTicket.priority == priority)
    if school_id:
        query = query.filter(SupportTicket.school_id == school_id)
    if assigned_to_id:
        query = query.filter(SupportTicket.assigned_to_id == assigned_to_id)
    return query.offset(skip).limit(limit).all()

async def update_support_ticket(
    db: Session,
    ticket_id: int,
    data: SupportTicketUpdate
) -> Optional[SupportTicket]:
    ticket = await get_support_ticket(db, ticket_id)
    if not ticket:
        return None

    # Update fields
    update_data = data.dict(exclude_unset=True)
    if "status" in update_data and update_data["status"] == TicketStatus.RESOLVED:
        update_data["resolved_at"] = datetime.utcnow()

    for field, value in update_data.items():
        setattr(ticket, field, value)

    db.commit()
    db.refresh(ticket)
    return ticket

# Ticket Comment Services
async def create_ticket_comment(
    db: Session,
    ticket_id: int,
    data: TicketCommentCreate,
    user_id: int
) -> TicketComment:
    # Verify ticket exists
    ticket = await get_support_ticket(db, ticket_id)
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )

    comment = TicketComment(
        **data.dict(),
        ticket_id=ticket_id,
        user_id=user_id
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment

async def get_ticket_comments(
    db: Session,
    ticket_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[TicketComment]:
    return db.query(TicketComment).filter(
        TicketComment.ticket_id == ticket_id
    ).offset(skip).limit(limit).all()

# Onboarding Task Services
async def create_onboarding_task(db: Session, data: OnboardingTaskCreate) -> OnboardingTask:
    task_data = data.dict(exclude={"dependencies"})
    task = OnboardingTask(**task_data)
    db.add(task)
    db.commit()

    # Add dependencies if provided
    if data.dependencies:
        for dep_id in data.dependencies:
            dep_task = await get_onboarding_task(db, dep_id)
            if dep_task:
                task.dependencies.append(dep_task)

    db.commit()
    db.refresh(task)
    return task

async def get_onboarding_task(db: Session, task_id: int) -> Optional[OnboardingTask]:
    return db.query(OnboardingTask).filter(OnboardingTask.id == task_id).first()

async def get_onboarding_tasks(
    db: Session,
    school_id: Optional[int] = None,
    status: Optional[str] = None,
    assigned_to_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100
) -> List[OnboardingTask]:
    query = db.query(OnboardingTask)
    if school_id:
        query = query.filter(OnboardingTask.school_id == school_id)
    if status:
        query = query.filter(OnboardingTask.status == status)
    if assigned_to_id:
        query = query.filter(OnboardingTask.assigned_to_id == assigned_to_id)
    return query.order_by(OnboardingTask.order).offset(skip).limit(limit).all()

async def update_onboarding_task(
    db: Session,
    task_id: int,
    data: OnboardingTaskUpdate
) -> Optional[OnboardingTask]:
    task = await get_onboarding_task(db, task_id)
    if not task:
        return None

    # Update fields
    update_data = data.dict(exclude={"dependencies"}, exclude_unset=True)
    if "status" in update_data and update_data["status"] == OnboardingTaskStatus.COMPLETED:
        update_data["completed_at"] = datetime.utcnow()

    for field, value in update_data.items():
        setattr(task, field, value)

    # Update dependencies if provided
    if data.dependencies is not None:
        task.dependencies = []
        for dep_id in data.dependencies:
            dep_task = await get_onboarding_task(db, dep_id)
            if dep_task:
                task.dependencies.append(dep_task)

    db.commit()
    db.refresh(task)
    return task