from sqlalchemy import text
from sqlalchemy.orm import Session
from app.core.config import get_settings
from app.models.user import User
from app.models.tenant import Tenant
from app.models.enums import UserRole
from app.models.saas import SaaSAdmin, SaaSRole
from app.core.security import get_password_hash

settings = get_settings()

def init_db(db: Session) -> None:
    # Create schemas
    schemas = [
        "system",      # For audit logs, settings, etc.
        "academic",    # For academic related tables
        "calendar",    # For calendar and events
        "resource",    # For resource booking
        "staff",       # For staff management
        "analytics"    # For analytics and reporting
    ]
    
    for schema in schemas:
        db.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema}"))
    
    db.commit()

    # Create default tenant if it doesn't exist
    default_tenant = db.query(Tenant).filter(Tenant.name == "Default Tenant").first()
    if not default_tenant:
        default_tenant = Tenant(
            name="Default Tenant",
            subdomain="default"  # Adding the required subdomain field
        )
        db.add(default_tenant)
        db.commit()
        db.refresh(default_tenant)

    # Create SaaS admin if it doesn't exist
    saas_admin = db.query(SaaSAdmin).filter(
        SaaSAdmin.email == settings.FIRST_SUPERUSER_EMAIL
    ).first()
    if not saas_admin:
        saas_admin = SaaSAdmin(
            username=settings.FIRST_SUPERUSER_USERNAME,
            email=settings.FIRST_SUPERUSER_EMAIL,
            hashed_password=get_password_hash(settings.FIRST_SUPERUSER_PASSWORD),
            role=SaaSRole.SUPER_ADMIN,
            is_active=True,
            full_name=settings.FIRST_SUPERUSER_FULL_NAME
        )
        db.add(saas_admin)
        db.commit()
        db.refresh(saas_admin)

if __name__ == "__main__":
    from app.db.session import SessionLocal
    
    db = SessionLocal()
    try:
        init_db(db)
        print("Database initialized successfully!")
    except Exception as e:
        print(f"Error initializing database: {e}")
        raise
    finally:
        db.close()