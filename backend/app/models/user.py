from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from app.models.enums import UserRole

class User(BaseModel):
    __tablename__ = "users"

    tenant_id = Column(Integer, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False)  # Store as string to avoid SQLite enum issues
    is_active = Column(Boolean, default=True, nullable=False)  # Changed to Boolean
    
    # Relationships
    tenant = relationship("Tenant", back_populates="users")