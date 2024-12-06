from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.security import get_password_hash
from app.models.user import User
from app.models.tenant import Tenant
from app.core.config import get_settings

settings = get_settings()

def create_superuser(
    email: str = "admin@example.com",
    password: str = "admin123",
    username: str = "admin",
) -> None:
    # Create database engine
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    try:
        # First create a default tenant
        tenant = db.query(Tenant).filter(Tenant.code == "system").first()
        if not tenant:
            tenant = Tenant(
                name="System",
                code="system",
                description="System tenant for superusers"
            )
            db.add(tenant)
            db.flush()

        # Check if superuser already exists
        user = db.query(User).filter(User.email == email).first()
        if user:
            print(f"Superuser with email {email} already exists")
            return

        # Create superuser
        superuser = User(
            email=email,
            username=username,
            hashed_password=get_password_hash(password),
            role="superuser",
            is_active="true",
            tenant_id=tenant.id
        )
        
        db.add(superuser)
        db.commit()
        print(f"Superuser created successfully with email: {email}")
    
    except Exception as e:
        print(f"Error creating superuser: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_superuser()