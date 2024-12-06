import typer
from sqlalchemy.orm import Session
from app.core.config import get_settings
from app.core.database import SessionLocal
from app.core.auth import get_password_hash
from app.models.enums import UserRole
from app.models.user import User
from app.models.tenant import Tenant

settings = get_settings()

def create_superuser(
    db: Session,
    username: str,
    email: str,
    password: str
) -> User:
    # Create system tenant if it doesn't exist
    system_tenant = db.query(Tenant).filter(
        Tenant.name == "System"
    ).first()
    
    if not system_tenant:
        system_tenant = Tenant(name="System")
        db.add(system_tenant)
        db.flush()
    
    # Check if superuser already exists
    existing_user = db.query(User).filter(
        User.email == email
    ).first()
    
    if existing_user:
        typer.echo(f"User with email {email} already exists")
        return existing_user
    
    # Create superuser
    superuser = User(
        tenant_id=system_tenant.id,
        username=username,
        email=email,
        hashed_password=get_password_hash(password),
        role=UserRole.SUPER_ADMIN,
        is_active=True
    )
    
    db.add(superuser)
    db.commit()
    db.refresh(superuser)
    
    return superuser

def main(
    username: str = typer.Option(..., prompt=True),
    email: str = typer.Option(..., prompt=True),
    password: str = typer.Option(..., prompt=True, hide_input=True),
    confirm_password: str = typer.Option(..., prompt=True, hide_input=True)
):
    if password != confirm_password:
        typer.echo("Error: Passwords don't match")
        raise typer.Exit(1)
    
    db = SessionLocal()
    try:
        user = create_superuser(db, username, email, password)
        typer.echo(f"Superuser created successfully: {user.email}")
    except Exception as e:
        typer.echo(f"Error creating superuser: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    typer.run(main)