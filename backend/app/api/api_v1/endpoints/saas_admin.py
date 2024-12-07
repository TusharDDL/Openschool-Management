from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.core.security import require_super_admin
from app.schemas.saas import (
    SaaSAdminCreate, SaaSAdminUpdate, SaaSAdminResponse,
    SupportTicketCreate, SupportTicketUpdate, SupportTicketResponse,
    OnboardingTaskCreate, OnboardingTaskUpdate, OnboardingTaskResponse,
    TicketCommentCreate, TicketCommentResponse
)
from app.services.saas import (
    create_saas_admin, get_saas_admin, get_saas_admins, update_saas_admin,
    create_support_ticket, get_support_ticket, get_support_tickets, update_support_ticket,
    create_onboarding_task, get_onboarding_task, get_onboarding_tasks, update_onboarding_task,
    create_ticket_comment, get_ticket_comments
)
from app.models.saas import SaaSAdmin, SupportTicket, OnboardingTask

router = APIRouter()

# SaaS Admin Routes
@router.post("/admins", response_model=SaaSAdminResponse)
async def create_admin(
    data: SaaSAdminCreate,
    db: Session = Depends(get_db),
    current_user: SaaSAdmin = Depends(require_super_admin)
):
    """Create a new SaaS admin (requires super_admin role)"""
    return await create_saas_admin(db, data)

@router.get("/admins", response_model=List[SaaSAdminResponse])
async def list_admins(
    role: Optional[str] = None,
    is_active: Optional[bool] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: SaaSAdmin = Depends(require_super_admin)
):
    """List all SaaS admins with optional filtering"""
    return await get_saas_admins(db, role=role, is_active=is_active, skip=skip, limit=limit)

@router.get("/admins/{admin_id}", response_model=SaaSAdminResponse)
async def get_admin(
    admin_id: int,
    db: Session = Depends(get_db),
    current_user: SaaSAdmin = Depends(require_super_admin)
):
    """Get a specific SaaS admin's details"""
    admin = await get_saas_admin(db, admin_id)
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Admin not found"
        )
    return admin

@router.put("/admins/{admin_id}", response_model=SaaSAdminResponse)
async def update_admin(
    admin_id: int,
    data: SaaSAdminUpdate,
    db: Session = Depends(get_db),
    current_user: SaaSAdmin = Depends(require_super_admin)
):
    """Update a SaaS admin's details"""
    admin = await update_saas_admin(db, admin_id, data)
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Admin not found"
        )
    return admin

# Support Ticket Routes
@router.post("/tickets", response_model=SupportTicketResponse)
async def create_ticket(
    data: SupportTicketCreate,
    db: Session = Depends(get_db),
    current_user: SaaSAdmin = Depends(get_current_user)
):
    """Create a new support ticket"""
    return await create_support_ticket(db, data, current_user.id)

@router.get("/tickets", response_model=List[SupportTicketResponse])
async def list_tickets(
    status: Optional[str] = None,
    priority: Optional[str] = None,
    school_id: Optional[int] = None,
    assigned_to_id: Optional[int] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: SaaSAdmin = Depends(get_current_user)
):
    """List support tickets with optional filtering"""
    return await get_support_tickets(
        db,
        status=status,
        priority=priority,
        school_id=school_id,
        assigned_to_id=assigned_to_id,
        skip=skip,
        limit=limit
    )

@router.get("/tickets/{ticket_id}", response_model=SupportTicketResponse)
async def get_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: SaaSAdmin = Depends(get_current_user)
):
    """Get a specific support ticket's details"""
    ticket = await get_support_ticket(db, ticket_id)
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )
    return ticket

@router.put("/tickets/{ticket_id}", response_model=SupportTicketResponse)
async def update_ticket(
    ticket_id: int,
    data: SupportTicketUpdate,
    db: Session = Depends(get_db),
    current_user: SaaSAdmin = Depends(get_current_user)
):
    """Update a support ticket"""
    ticket = await update_support_ticket(db, ticket_id, data)
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )
    return ticket

@router.post("/tickets/{ticket_id}/comments", response_model=TicketCommentResponse)
async def add_ticket_comment(
    ticket_id: int,
    data: TicketCommentCreate,
    db: Session = Depends(get_db),
    current_user: SaaSAdmin = Depends(get_current_user)
):
    """Add a comment to a support ticket"""
    return await create_ticket_comment(db, ticket_id, data, current_user.id)

@router.get("/tickets/{ticket_id}/comments", response_model=List[TicketCommentResponse])
async def list_ticket_comments(
    ticket_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: SaaSAdmin = Depends(get_current_user)
):
    """List comments for a specific ticket"""
    return await get_ticket_comments(db, ticket_id, skip=skip, limit=limit)

# Onboarding Task Routes
@router.post("/tasks", response_model=OnboardingTaskResponse)
async def create_task(
    data: OnboardingTaskCreate,
    db: Session = Depends(get_db),
    current_user: SaaSAdmin = Depends(get_current_user)
):
    """Create a new onboarding task"""
    return await create_onboarding_task(db, data)

@router.get("/tasks", response_model=List[OnboardingTaskResponse])
async def list_tasks(
    school_id: Optional[int] = None,
    status: Optional[str] = None,
    assigned_to_id: Optional[int] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: SaaSAdmin = Depends(get_current_user)
):
    """List onboarding tasks with optional filtering"""
    return await get_onboarding_tasks(
        db,
        school_id=school_id,
        status=status,
        assigned_to_id=assigned_to_id,
        skip=skip,
        limit=limit
    )

@router.get("/tasks/{task_id}", response_model=OnboardingTaskResponse)
async def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: SaaSAdmin = Depends(get_current_user)
):
    """Get a specific onboarding task's details"""
    task = await get_onboarding_task(db, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task

@router.put("/tasks/{task_id}", response_model=OnboardingTaskResponse)
async def update_task(
    task_id: int,
    data: OnboardingTaskUpdate,
    db: Session = Depends(get_db),
    current_user: SaaSAdmin = Depends(get_current_user)
):
    """Update an onboarding task"""
    task = await update_onboarding_task(db, task_id, data)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task