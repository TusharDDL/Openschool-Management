# OpenHands School Management System - Backend Documentation

## Table of Contents
1. [Overview](#overview)
2. [Technology Stack](#technology-stack)
3. [Project Structure](#project-structure)
4. [API Documentation](#api-documentation)
5. [Database Models](#database-models)
6. [Authentication & Authorization](#authentication--authorization)
7. [Development Guide](#development-guide)

## Overview

OpenHands is a comprehensive school management system built with FastAPI and PostgreSQL. It follows a multi-tenant architecture where each school is a separate tenant, ensuring complete data isolation.

### Key Features
- Multi-tenant architecture
- Role-based access control (RBAC)
- JWT authentication
- Real-time data validation
- Automatic API documentation
- Database migrations
- Redis caching
- Rate limiting

## Technology Stack

- **Framework**: FastAPI 0.100+
- **Database**: PostgreSQL 14+
- **ORM**: SQLAlchemy 2.0+
- **Authentication**: JWT (JSON Web Tokens)
- **Caching**: Redis
- **Documentation**: OpenAPI/Swagger
- **Migrations**: Alembic

## Project Structure

\`\`\`
backend/
├── app/
│   ├── api/
│   │   └── api_v1/
│   │       ├── endpoints/
│   │       │   ├── academic.py      # Academic management
│   │       │   ├── auth.py         # Authentication
│   │       │   ├── schools.py      # School management
│   │       │   ├── students.py     # Student management
│   │       │   ├── subjects.py     # Subject management
│   │       │   ├── tenants.py      # Tenant management
│   │       │   └── timetable.py    # Timetable management
│   │       └── api.py
│   ├── core/
│   │   ├── config.py       # Configuration settings
│   │   ├── security.py     # Security utilities
│   │   └── database.py     # Database connection
│   ├── crud/
│   │   ├── academic.py     # Academic CRUD operations
│   │   ├── school.py       # School CRUD operations
│   │   └── user.py         # User CRUD operations
│   ├── models/
│   │   ├── academic_core.py    # Academic models
│   │   ├── user.py            # User models
│   │   └── tenant.py          # Tenant models
│   └── schemas/
│       ├── academic.py     # Academic Pydantic schemas
│       ├── auth.py        # Authentication schemas
│       └── base.py        # Base schemas
\`\`\`

## API Documentation

### 1. Authentication API (/api/v1/auth)

#### Login
\`\`\`http
POST /api/v1/auth/login
Content-Type: application/json

{
    "email": "admin@example.com",
    "password": "password123"
}

Response:
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1...",
    "token_type": "bearer"
}
\`\`\`

### 2. Academic Management (/api/v1/academic)

#### Academic Years
\`\`\`http
# Create Academic Year
POST /api/v1/academic/years
{
    "name": "2024-25",
    "start_date": "2024-04-01",
    "end_date": "2025-03-31",
    "is_active": true,
    "tenant_id": 1,
    "school_id": 1
}

# List Academic Years
GET /api/v1/academic/years?skip=0&limit=100&is_active=true

# Get Academic Year
GET /api/v1/academic/years/{id}

# Update Academic Year
PUT /api/v1/academic/years/{id}
\`\`\`

#### Classes
\`\`\`http
# Create Class
POST /api/v1/academic/classes
{
    "name": "Class 10",
    "grade_level": 10,
    "academic_year_id": 1,
    "is_active": true,
    "tenant_id": 1,
    "school_id": 1
}

# List Classes
GET /api/v1/academic/classes

# Get Class
GET /api/v1/academic/classes/{id}

# Update Class
PUT /api/v1/academic/classes/{id}
\`\`\`

#### Sections
\`\`\`http
# Create Section
POST /api/v1/academic/sections
{
    "name": "Section A",
    "class_id": 1,
    "capacity": 40,
    "is_active": true,
    "tenant_id": 1
}

# List Sections
GET /api/v1/academic/sections

# Get Section
GET /api/v1/academic/sections/{id}

# Update Section
PUT /api/v1/academic/sections/{id}
\`\`\`

### 3. Subject Management (/api/v1/subjects)

\`\`\`http
# Create Subject
POST /api/v1/subjects
{
    "name": "Mathematics",
    "code": "MATH10",
    "description": "Mathematics for Class 10",
    "credits": 5.0,
    "is_active": true,
    "tenant_id": 1,
    "school_id": 1
}

# List Subjects
GET /api/v1/subjects?skip=0&limit=100&is_active=true

# Get Subject
GET /api/v1/subjects/{id}

# Update Subject
PUT /api/v1/subjects/{id}
\`\`\`

### 4. Student Management (/api/v1/students)

\`\`\`http
# Create Student
POST /api/v1/students
{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "tenant_id": 1,
    "school_id": 1
}

# List Students
GET /api/v1/students

# Get Student
GET /api/v1/students/{id}

# Update Student
PUT /api/v1/students/{id}
\`\`\`

### 5. Attendance Management (/api/v1/attendance)

\`\`\`http
# Record Attendance
POST /api/v1/attendance
{
    "student_id": 1,
    "section_id": 1,
    "date": "2024-01-01",
    "status": "present",
    "tenant_id": 1
}

# Get Attendance
GET /api/v1/attendance?student_id=1&date=2024-01-01
\`\`\`

### 6. Fee Management (/api/v1/fees)

\`\`\`http
# Create Fee Structure
POST /api/v1/fees
{
    "name": "Tuition Fee",
    "amount": 5000,
    "due_date": "2024-01-01",
    "tenant_id": 1
}

# List Fees
GET /api/v1/fees

# Get Fee Details
GET /api/v1/fees/{id}
\`\`\`

### 7. School Management (/api/v1/schools)

\`\`\`http
# Create School
POST /api/v1/schools
{
    "name": "Example School",
    "address": "123 Main St",
    "contact_email": "info@school.com",
    "contact_phone": "1234567890",
    "tenant_id": 1
}

# List Schools
GET /api/v1/schools

# Get School
GET /api/v1/schools/{id}

# Update School
PUT /api/v1/schools/{id}
\`\`\`

### 8. Tenant Management (/api/v1/tenants)

\`\`\`http
# Create Tenant
POST /api/v1/tenants
{
    "name": "Example Organization",
    "domain": "example.com",
    "is_active": true
}

# List Tenants
GET /api/v1/tenants

# Get Tenant
GET /api/v1/tenants/{id}

# Update Tenant
PUT /api/v1/tenants/{id}
\`\`\`

### 9. Timetable Management (/api/v1/academic/timetable)

\`\`\`http
# Create Timetable Entry
POST /api/v1/academic/timetable
{
    "section_id": 1,
    "subject_id": 1,
    "teacher_id": 1,
    "day": "monday",
    "start_time": "09:00:00",
    "end_time": "10:00:00"
}

# List Timetable
GET /api/v1/academic/timetable?section_id=1

# Get Timetable Entry
GET /api/v1/academic/timetable/{id}

# Update Timetable Entry
PUT /api/v1/academic/timetable/{id}
\`\`\`

## Database Models

### Core Models

1. **BaseModel**
\`\`\`python
class BaseModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
\`\`\`

2. **TenantModel**
\`\`\`python
class TenantModel(BaseModel):
    __abstract__ = True
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
\`\`\`

### Academic Models

1. **AcademicYear**
\`\`\`python
class AcademicYear(TenantModel):
    __tablename__ = "academic_years"
    name = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    is_active = Column(Boolean, default=True)
    school_id = Column(Integer, ForeignKey("schools.id"))
\`\`\`

2. **Class**
\`\`\`python
class Class(TenantModel):
    __tablename__ = "classes"
    name = Column(String, nullable=False)
    grade_level = Column(Integer, nullable=False)
    academic_year_id = Column(Integer, ForeignKey("academic_years.id"))
    is_active = Column(Boolean, default=True)
    school_id = Column(Integer, ForeignKey("schools.id"))
\`\`\`

3. **Section**
\`\`\`python
class Section(TenantModel):
    __tablename__ = "sections"
    name = Column(String, nullable=False)
    class_id = Column(Integer, ForeignKey("classes.id"))
    capacity = Column(Integer)
    is_active = Column(Boolean, default=True)
\`\`\`

4. **Subject**
\`\`\`python
class Subject(TenantModel):
    __tablename__ = "subjects"
    name = Column(String, nullable=False)
    code = Column(String, nullable=False)
    description = Column(String)
    credits = Column(Float)
    is_active = Column(Boolean, default=True)
    school_id = Column(Integer, ForeignKey("schools.id"))
\`\`\`

### User Models

1. **User**
\`\`\`python
class User(TenantModel):
    __tablename__ = "users"
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(Enum(UserRole), nullable=False)
    school_id = Column(Integer, ForeignKey("schools.id"))
\`\`\`

2. **Student**
\`\`\`python
class Student(TenantModel):
    __tablename__ = "students"
    user_id = Column(Integer, ForeignKey("users.id"))
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    date_of_birth = Column(Date)
    admission_number = Column(String)
    school_id = Column(Integer, ForeignKey("schools.id"))
\`\`\`

## Authentication & Authorization

### JWT Authentication
- Token-based authentication using JWT
- Token expiration and refresh mechanism
- Role-based access control

### Role Hierarchy
\`\`\`python
ROLE_HIERARCHY = {
    UserRole.SUPER_ADMIN: 100,
    UserRole.SCHOOL_ADMIN: 90,
    UserRole.TEACHER: 80,
    UserRole.STUDENT: 70,
    UserRole.PARENT: 60,
}
\`\`\`

### Permission Decorators
\`\`\`python
def require_role(required_role: UserRole):
    async def role_checker(current_user: User = Depends(get_current_user)):
        if not check_permission(required_role, current_user.role):
            raise HTTPException(
                status_code=403,
                detail=f"Role {required_role} or higher required"
            )
        return current_user
    return role_checker
\`\`\`

## Development Guide

### Setting Up Development Environment

1. **Clone the Repository**
\`\`\`bash
git clone <repository-url>
cd backend
\`\`\`

2. **Create Virtual Environment**
\`\`\`bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\\Scripts\\activate  # Windows
\`\`\`

3. **Install Dependencies**
\`\`\`bash
pip install -r requirements.txt
\`\`\`

4. **Environment Variables**
Create a .env file:
\`\`\`env
DATABASE_URL=postgresql://user:password@localhost:5432/db_name
SECRET_KEY=your-secret-key
REDIS_URL=redis://localhost:6379
\`\`\`

5. **Database Setup**
\`\`\`bash
# Apply migrations
alembic upgrade head

# Create initial admin user
python -m app.scripts.create_admin
\`\`\`

6. **Run Development Server**
\`\`\`bash
uvicorn app.main:app --reload
\`\`\`

### API Testing

You can test the APIs using the Swagger documentation at:
\`http://localhost:8000/docs\`

Example using curl:
\`\`\`bash
# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "Admin123"}'

# Create Academic Year (with token)
curl -X POST http://localhost:8000/api/v1/academic/years \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "2024-25",
    "start_date": "2024-04-01",
    "end_date": "2025-03-31",
    "is_active": true,
    "tenant_id": 1,
    "school_id": 1
  }'
\`\`\`

### Common Issues and Solutions

1. **Database Connection Issues**
   - Check if PostgreSQL is running
   - Verify DATABASE_URL in .env
   - Ensure database exists

2. **Migration Issues**
   - Run \`alembic history\` to check migration state
   - Use \`alembic stamp head\` to mark all migrations as complete
   - Delete migrations folder and recreate if needed

3. **Authentication Issues**
   - Check if SECRET_KEY is set correctly
   - Verify token expiration time
   - Ensure user exists in database

### Best Practices

1. **Code Organization**
   - Keep related functionality together
   - Use meaningful file and directory names
   - Follow Python naming conventions

2. **API Design**
   - Use proper HTTP methods
   - Return appropriate status codes
   - Include error messages in responses
   - Validate input data

3. **Security**
   - Always validate input data
   - Use proper authentication
   - Implement rate limiting
   - Sanitize database queries

4. **Performance**
   - Use database indexes
   - Implement caching
   - Optimize database queries
   - Use async operations when appropriate

## Conclusion

This backend implementation provides a robust foundation for the school management system. It's designed to be scalable, maintainable, and secure. The multi-tenant architecture ensures proper data isolation, while the role-based access control system provides flexible permission management.

For any questions or issues, please refer to the GitHub repository or contact the development team.