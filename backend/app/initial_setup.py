from app.db.session import SessionLocal
from app.models.tenant import Tenant
from app.models.saas import SaaSAdmin, SaaSRole
from app.core.security import get_password_hash
from app.core.config import settings

def init_db():
    db = SessionLocal()
    try:
        # Create default tenant
        tenant = db.query(Tenant).filter(Tenant.name == "Default School").first()
        if not tenant:
            tenant = Tenant(
                name="Default School",
                subdomain="default-school"  # Adding the required subdomain
            )
            db.add(tenant)
            db.flush()
        
        # Create super admin if it doesn't exist
        super_admin = db.query(SaaSAdmin).filter(
            SaaSAdmin.email == settings.FIRST_SUPERUSER_EMAIL
        ).first()
        if not super_admin:
            super_admin = SaaSAdmin(
                email=settings.FIRST_SUPERUSER_EMAIL,
                username=settings.FIRST_SUPERUSER_USERNAME,
                hashed_password=get_password_hash(settings.FIRST_SUPERUSER_PASSWORD),
                role=SaaSRole.SUPER_ADMIN,
                is_active=True,
                full_name=settings.FIRST_SUPERUSER_FULL_NAME
            )
            db.add(super_admin)

        db.commit()
        print("Database initialized successfully!")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    init_db()