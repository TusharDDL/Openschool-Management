import typer
from sqlalchemy.orm import Session
from app.core.config import get_settings
from app.core.database import SessionLocal
from app.core.security import get_password_hash
from app.models.saas import SaaSAdmin, SaaSRole

settings = get_settings()

def create_saas_superadmin(
    db: Session,
    username: str,
    email: str,
    password: str,
    full_name: str
) -> SaaSAdmin:
    # Check if admin already exists
    existing_admin = db.query(SaaSAdmin).filter(
        SaaSAdmin.email == email
    ).first()
    
    if existing_admin:
        typer.echo(f"Admin with email {email} already exists")
        return existing_admin
    
    # Create super admin
    admin = SaaSAdmin(
        username=username,
        email=email,
        hashed_password=get_password_hash(password),
        role=SaaSRole.SUPER_ADMIN,
        full_name=full_name,
        is_active=True
    )
    
    db.add(admin)
    db.commit()
    db.refresh(admin)
    
    return admin

def main():
    username = "admin"
    email = "admin@example.com"
    password = "Admin123!"
    full_name = "System Administrator"
    
    db = SessionLocal()
    try:
        admin = create_saas_superadmin(db, username, email, password, full_name)
        typer.echo(f"SaaS super admin created successfully: {admin.email}")
    except Exception as e:
        typer.echo(f"Error creating SaaS super admin: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main()