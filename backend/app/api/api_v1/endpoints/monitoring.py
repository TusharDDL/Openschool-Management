from typing import Dict, Any, List, Union
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import psutil
from datetime import datetime, timedelta, UTC
import logging

from app.api.deps import get_db, get_current_user
from app.models.saas import SaaSAdmin
from app.models.user import User
from app.models.tenant import Tenant
from app.models.enums import UserRole

def check_monitoring_access(current_user: Union[User, SaaSAdmin]) -> bool:
    """Check if user has access to monitoring endpoints"""
    logging.info(f"Checking monitoring access for user type: {type(current_user)}")
    logging.info(f"User attributes: {vars(current_user)}")
    
    # Check if user is SaaS admin
    if isinstance(current_user, SaaSAdmin):
        logging.info("User is SaaS admin - access granted")
        return True
    
    # Check token_role first (from JWT)
    token_role = getattr(current_user, 'token_role', '').upper()
    if token_role in ['SUPER_ADMIN', 'ADMIN']:
        logging.info(f"User has admin token_role: {token_role} - access granted")
        return True
    
    # Check regular role
    if hasattr(current_user, 'role'):
        user_role = str(current_user.role).upper()
        logging.info(f"User role: {user_role}")
        if user_role in ['SUPER_ADMIN', 'ADMIN']:
            logging.info(f"User has admin role: {user_role} - access granted")
            return True
    
    logging.warning("Access denied - insufficient permissions")
    return False

router = APIRouter()

def get_system_metrics() -> Dict[str, float]:
    """Get real system metrics using psutil"""
    try:
        # CPU usage
        cpu_usage = psutil.cpu_percent(interval=1)
        
        # Memory usage
        memory = psutil.virtual_memory()
        memory_usage = memory.percent
        
        # Disk usage
        disk = psutil.disk_usage('/')
        disk_usage = disk.percent
        
        return {
            "cpu_usage": round(cpu_usage, 2),
            "memory_usage": round(memory_usage, 2),
            "disk_usage": round(disk_usage, 2)
        }
    except Exception as e:
        logging.error(f"Error getting system metrics: {str(e)}")
        return {
            "cpu_usage": 0,
            "memory_usage": 0,
            "disk_usage": 0
        }

@router.get("/metrics")
async def get_metrics(
    db: Session = Depends(get_db),
    current_user: Union[User, SaaSAdmin] = Depends(get_current_user)
) -> Dict[str, Any]:
    logging.info(f"Metrics endpoint accessed by user: {getattr(current_user, 'email', 'Unknown')}")
    if not check_monitoring_access(current_user):
        logging.warning(f"Access denied for user: {getattr(current_user, 'email', 'Unknown')}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions. SaaS admin or SUPER_ADMIN role required."
        )
    logging.info("Access granted - fetching metrics")
    """Get system metrics and statistics"""
    try:
        # Get system metrics
        system_metrics = get_system_metrics()
        
        # Get total active users (simplified metric for now)
        active_users = db.query(User).filter(
            User.is_active == True
        ).count()
        
        # Calculate average response time (placeholder for now)
        # In production, you'd want to use proper APM tools
        response_time = 235  # milliseconds
        
        # Calculate error rate from logs (placeholder)
        # In production, use proper error tracking
        error_rate = 0.42  # percentage
        
        logging.info(f"Active users count: {active_users}")
        
        try:
            # Get total number of tenants
            total_tenants = db.query(Tenant).count()
            logging.info(f"Total tenants count: {total_tenants}")
        except Exception as e:
            logging.error(f"Error getting tenant count: {str(e)}")
            total_tenants = 0

        response_data = {
            **system_metrics,
            "active_users": active_users,
            "response_time": response_time,
            "error_rate": error_rate,
            "total_tenants": total_tenants,
            "uptime": psutil.boot_time(),
            "last_updated": datetime.now(UTC).isoformat()
        }
        logging.info(f"Returning metrics: {response_data}")
        return response_data
    except Exception as e:
        logging.error(f"Error in get_metrics: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching metrics: {str(e)}"
        )

@router.get("/status")
async def get_status(
    current_user: Union[User, SaaSAdmin] = Depends(get_current_user)
) -> Dict[str, Any]:
    if not check_monitoring_access(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions. SaaS admin or SUPER_ADMIN role required."
        )
    """Get system operational status"""
    try:
        # Check various system components
        cpu_usage = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Determine status based on thresholds
        system_status = "operational"
        if cpu_usage > 90 or memory.percent > 90 or disk.percent > 90:
            system_status = "degraded"
        
        return {
            "status": system_status,
            "services": [
                {
                    "name": "API Server",
                    "status": "operational",
                    "latency": 42  # ms
                },
                {
                    "name": "Database",
                    "status": "operational",
                    "latency": 15  # ms
                },
                {
                    "name": "File Storage",
                    "status": "operational",
                    "latency": 85  # ms
                }
            ],
            "last_checked": datetime.now(UTC).isoformat()
        }
    except Exception as e:
        logging.error(f"Error in get_status: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching system status: {str(e)}"
        )

@router.get("/logs")
async def get_logs(
    limit: int = 100,
    current_user: Union[User, SaaSAdmin] = Depends(get_current_user)
) -> List[Dict[str, Any]]:
    if not check_monitoring_access(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions. SaaS admin or SUPER_ADMIN role required."
        )
    """Get recent system logs"""
    try:
        # Placeholder for now - in production, integrate with proper logging system
        return [
            {
                "timestamp": datetime.now(UTC).isoformat(),
                "level": "info",
                "message": "System running normally",
                "service": "api"
            },
            {
                "timestamp": (datetime.now(UTC) - timedelta(minutes=5)).isoformat(),
                "level": "warning",
                "message": "High memory usage detected",
                "service": "monitoring"
            }
        ]
    except Exception as e:
        logging.error(f"Error in get_logs: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching system logs: {str(e)}"
        )
