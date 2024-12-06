from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine, Base
from app.models.tenant import Tenant
from app.models.user import User
from app.core.security import get_password_hash
from app.models.enums import UserRole

def init_db():
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Create default tenant
        if not db.query(Tenant).filter(Tenant.name == "Default School").first():
            default_tenant = Tenant(
                name="Default School"
            )
            db.add(default_tenant)
            db.commit()
            db.refresh(default_tenant)
            
            # Create super admin user
            if not db.query(User).filter(User.email == "admin@school.com").first():
                super_admin = User(
                    email="admin@school.com",
                    username="admin",
                    hashed_password=get_password_hash("admin123"),
                    role=UserRole.SUPER_ADMIN,
                    tenant_id=default_tenant.id,
                    is_active="true"  # SQLite enum value
                )
                db.add(super_admin)
                db.commit()
                
                print("Created default tenant and super admin user:")
                print("Email: admin@school.com")
                print("Password: admin123")
    
    finally:
        db.close()

if __name__ == "__main__":
    init_db()