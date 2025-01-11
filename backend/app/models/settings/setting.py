from enum import Enum
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum as SQLEnum, Text, JSON, UniqueConstraint
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class SettingType(str, Enum):
    SYSTEM = "SYSTEM"
    TENANT = "TENANT"
    SCHOOL = "SCHOOL"
    USER = "USER"

class SettingDataType(str, Enum):
    STRING = "STRING"
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    BOOLEAN = "BOOLEAN"
    JSON = "JSON"
    DATE = "DATE"
    TIME = "TIME"
    DATETIME = "DATETIME"

class SettingCategory(str, Enum):
    GENERAL = "GENERAL"
    ACADEMIC = "ACADEMIC"
    ATTENDANCE = "ATTENDANCE"
    EXAM = "EXAM"
    FINANCE = "FINANCE"
    TRANSPORT = "TRANSPORT"
    HOSTEL = "HOSTEL"
    LIBRARY = "LIBRARY"
    COMMUNICATION = "COMMUNICATION"
    SECURITY = "SECURITY"
    INTEGRATION = "INTEGRATION"
    OTHER = "OTHER"

class Setting(BaseModel):
    __tablename__ = "settings"
    __table_args__ = (
        UniqueConstraint('tenant_id', 'school_id', 'user_id', 'key', name='uq_setting'),
        {'schema': 'settings'}
    )

    tenant_id = Column(Integer, ForeignKey("public.tenants.id", ondelete="CASCADE"))
    school_id = Column(Integer, ForeignKey("public.schools.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("public.users.id", ondelete="CASCADE"))
    
    key = Column(String, nullable=False)
    value = Column(String)  # All values stored as strings and converted based on data_type
    data_type = Column(SQLEnum(SettingDataType), nullable=False)
    setting_type = Column(SQLEnum(SettingType), nullable=False)
    category = Column(SQLEnum(SettingCategory), nullable=False)
    description = Column(Text)
    is_system = Column(Boolean, default=False)  # System settings can't be modified by users
    is_public = Column(Boolean, default=False)  # Public settings are visible to all users
    is_encrypted = Column(Boolean, default=False)  # For sensitive settings like API keys
    validation_rules = Column(JSON)  # JSON Schema for validation
    default_value = Column(String)
    options = Column(JSON)  # For settings with predefined options
    is_required = Column(Boolean, default=False)
    depends_on = Column(String)  # Key of another setting this depends on
    is_active = Column(Boolean, default=True)

    # Relationships
    tenant = relationship("Tenant")
    school = relationship("School")
    user = relationship("User")

class SettingGroup(BaseModel):
    __tablename__ = "setting_groups"
    __table_args__ = (
        UniqueConstraint('tenant_id', 'code', name='uq_setting_group'),
        {'schema': 'settings'}
    )

    tenant_id = Column(Integer, ForeignKey("public.tenants.id", ondelete="CASCADE"))
    
    code = Column(String, nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text)
    category = Column(SQLEnum(SettingCategory), nullable=False)
    setting_type = Column(SQLEnum(SettingType), nullable=False)
    order = Column(Integer, default=0)
    is_system = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    # Relationships
    tenant = relationship("Tenant")
    settings = relationship("GroupSetting", back_populates="group", cascade="all, delete-orphan")

class GroupSetting(BaseModel):
    __tablename__ = "group_settings"
    __table_args__ = (
        UniqueConstraint('group_id', 'setting_id', name='uq_group_setting'),
        {'schema': 'settings'}
    )

    group_id = Column(Integer, ForeignKey("settings.setting_groups.id", ondelete="CASCADE"), nullable=False)
    setting_id = Column(Integer, ForeignKey("settings.settings.id", ondelete="CASCADE"), nullable=False)
    
    order = Column(Integer, default=0)
    is_required = Column(Boolean, default=False)
    is_visible = Column(Boolean, default=True)
    depends_on = Column(String)  # JSON object defining dependencies

    # Relationships
    group = relationship("SettingGroup", back_populates="settings")
    setting = relationship("Setting")

class SettingAudit(BaseModel):
    __tablename__ = "setting_audits"
    __table_args__ = {'schema': 'settings'}

    setting_id = Column(Integer, ForeignKey("settings.settings.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("public.users.id", ondelete="CASCADE"), nullable=False)
    
    old_value = Column(String)
    new_value = Column(String)
    action = Column(String, nullable=False)  # CREATE, UPDATE, DELETE
    ip_address = Column(String)
    user_agent = Column(String)
    reason = Column(Text)

    # Relationships
    setting = relationship("Setting")
    user = relationship("User")