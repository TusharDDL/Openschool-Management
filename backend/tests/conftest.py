import pytest
from typing import Generator, Dict
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import get_settings
from app.core.database import Base, get_db
from app.main import app
from app.models.user import User
from app.models.tenant import Tenant
from app.models.enums import UserRole
from app.core.auth import create_access_token, get_password_hash

settings = get_settings()

# Use in-memory SQLite for tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def db() -> Generator:
    # Create the database and tables
    Base.metadata.create_all(bind=engine)
    
    # Create a session
    session = TestingSessionLocal()
    
    try:
        yield session
    finally:
        session.close()
        # Drop all tables after tests
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="session")
def client(db: TestingSessionLocal) -> Generator:
    # Override the get_db dependency
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture(scope="session")
def test_tenant(db: TestingSessionLocal) -> Tenant:
    tenant = Tenant(name="Test School District")
    db.add(tenant)
    db.commit()
    db.refresh(tenant)
    return tenant

@pytest.fixture(scope="session")
def test_users(db: TestingSessionLocal, test_tenant: Tenant) -> Dict[str, User]:
    users = {}
    
    # Create users with different roles
    roles = [
        (UserRole.SUPER_ADMIN, "superadmin"),
        (UserRole.SCHOOL_ADMIN, "schooladmin"),
        (UserRole.TEACHER, "teacher"),
        (UserRole.STUDENT, "student"),
        (UserRole.PARENT, "parent")
    ]
    
    for role, username in roles:
        user = User(
            tenant_id=test_tenant.id,
            username=username,
            email=f"{username}@test.com",
            hashed_password=get_password_hash(f"{username}123"),
            role=role,
            is_active=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        users[role] = user
    
    return users

@pytest.fixture(scope="session")
def test_tokens(test_users: Dict[str, User]) -> Dict[str, str]:
    return {
        role: create_access_token(user)
        for role, user in test_users.items()
    }

@pytest.fixture(scope="session")
def superadmin_token(test_tokens: Dict[str, str]) -> str:
    return test_tokens[UserRole.SUPER_ADMIN]

@pytest.fixture(scope="session")
def schooladmin_token(test_tokens: Dict[str, str]) -> str:
    return test_tokens[UserRole.SCHOOL_ADMIN]

@pytest.fixture(scope="session")
def teacher_token(test_tokens: Dict[str, str]) -> str:
    return test_tokens[UserRole.TEACHER]

@pytest.fixture(scope="session")
def student_token(test_tokens: Dict[str, str]) -> str:
    return test_tokens[UserRole.STUDENT]

@pytest.fixture(scope="session")
def parent_token(test_tokens: Dict[str, str]) -> str:
    return test_tokens[UserRole.PARENT]