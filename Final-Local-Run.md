# Local Development Setup Guide

This guide provides step-by-step instructions for setting up the School Management System on your local machine.

## Prerequisites

### Required Software
1. **Node.js** (v18.x or higher)
   - Download from: https://nodejs.org/

2. **Python** (v3.11 or higher)
   - Download from: https://www.python.org/downloads/

3. **PostgreSQL** (v15.x)
   - Download from: https://www.postgresql.org/download/
   - Windows: Use the installer
   - Mac: `brew install postgresql@15`
   - Linux: `sudo apt install postgresql postgresql-contrib`

4. **Redis** (v7.x)
   - Windows: https://github.com/microsoftarchive/redis/releases
   - Mac: `brew install redis`
   - Linux: `sudo apt install redis-server`

### System Requirements
- CPU: 2+ cores recommended
- RAM: 4GB minimum, 8GB recommended
- Storage: 10GB free space
- Internet connection for package installation

## Setup Steps

### 1. Database Setup

```bash
# Start PostgreSQL service
# Windows: Use Services app
# Mac: brew services start postgresql
# Linux: sudo service postgresql start

# Start Redis service
# Windows: Use Services app
# Mac: brew services start redis
# Linux: sudo service redis-server start

# Create database and user
# Windows: Run as administrator
# Mac/Linux: Run as postgres user
psql -U postgres

# In PostgreSQL prompt:
CREATE USER school_user WITH PASSWORD 'school_password' SUPERUSER;
CREATE DATABASE school_management;
GRANT ALL PRIVILEGES ON DATABASE school_management TO school_user;
\c school_management
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
\q
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOL
# Database
DATABASE_URL=postgresql://school_user:school_password@localhost:5432/school_management
ASYNC_DATABASE_URL=postgresql+asyncpg://school_user:school_password@localhost:5432/school_management

# Redis
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=your-secret-key-at-least-32-characters-long
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
ALGORITHM=HS256

# API Settings
API_V1_STR=/api/v1
PROJECT_NAME=School Management System
VERSION=1.0.0

# CORS Settings
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:8000"]

# File Storage
UPLOAD_DIR=uploads
MAX_UPLOAD_SIZE=5242880

# Email Settings
SMTP_TLS=True
SMTP_PORT=587
SMTP_HOST=smtp.gmail.com
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-specific-password
EMAILS_FROM_EMAIL=your-email@gmail.com
EMAILS_FROM_NAME=School Management System

# First Super Admin
FIRST_SUPERUSER_EMAIL=admin@example.com
FIRST_SUPERUSER_PASSWORD=Admin123
EOL

# Initialize database and create first superuser
python -m app.initial_setup

# Run database migrations
export PYTHONPATH=$PWD
alembic upgrade head

# Create initial data
python -m app.scripts.seed_data

# Start backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Frontend Setup

```bash
# Navigate to project root
cd ..

# Install dependencies
npm install

# Create .env.local file
cat > .env.local << EOL
# API URLs
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_WEBSOCKET_URL=ws://localhost:8000/ws
NEXT_PUBLIC_UPLOAD_URL=http://localhost:8000/uploads

# File Upload
NEXT_PUBLIC_MAX_FILE_SIZE=5242880
NEXT_PUBLIC_ALLOWED_FILE_TYPES=".pdf,.doc,.docx,.xls,.xlsx,.jpg,.jpeg,.png"

# Authentication
NEXT_PUBLIC_JWT_EXPIRES_IN=30
NEXT_PUBLIC_REFRESH_TOKEN_EXPIRES_IN=7

# Features
NEXT_PUBLIC_ENABLE_THEME=true
NEXT_PUBLIC_ENABLE_RTL=true
NEXT_PUBLIC_ENABLE_MOCK_API=false
NEXT_PUBLIC_ENABLE_REDUX_LOGGER=true

# Analytics
NEXT_PUBLIC_GA_TRACKING_ID=
NEXT_PUBLIC_ENABLE_ANALYTICS=false
EOL

# Start frontend development server
npm run dev
```

## Accessing the Application

1. Frontend: http://localhost:3000
2. Backend API: http://localhost:8000
3. API Documentation: http://localhost:8000/docs
4. Admin Dashboard: http://localhost:3000/dashboard/admin

## User Roles and Access

### 1. SaaS Admin (Super Admin)
- **Credentials:**
  - Email: saas.admin@example.com
  - Password: SaasAdmin123!
- **Access URL:** http://localhost:3000/dashboard/admin
- **Features:**
  - Tenant Management
  - System Monitoring
  - Support Tickets
  - Board Reports
  - School Registration

### 2. School Admin
- **Test Credentials:**
  - Email: school.admin@example.com
  - Password: SchoolAdmin456!
- **Access URL:** http://localhost:3000/dashboard/admin
- **Features:**
  - Student Management
  - Academic Management
  - Fee Management
  - Staff Management
  - Reports Generation

### 3. Parent Portal
- **Test Credentials:**
  - Email: parent.user@example.com
  - Password: ParentUser789!
- **Access URL:** http://localhost:3000/dashboard/parent
- **Features:**
  - View Children's Progress
  - Attendance Tracking
  - Fee Payment
  - Parent-Teacher Meetings
  - Communication

## Multi-Tenant Architecture

The system uses a multi-tenant architecture where:
1. Each school is a separate tenant
2. Data is isolated between tenants
3. SaaS admin manages all tenants
4. School admin manages their specific tenant
5. Users (teachers, students, parents) belong to specific tenants

### Tenant Isolation
- Database level isolation using tenant_id
- API level access control
- Role-based permissions within tenants
- Separate file storage per tenant

## API Integration Guide

### 1. Authentication Flow
```typescript
// Login Request
POST /api/v1/auth/login
{
  "email": "user@example.com",
  "password": "password"
}

// Response
{
  "access_token": "JWT_TOKEN",
  "token_type": "bearer"
}
```

### 2. Role-Based Endpoints
- SaaS Admin: `/api/v1/tenants`, `/api/v1/monitoring`
- School Admin: `/api/v1/schools`, `/api/v1/academic`
- Parent: `/api/v1/parent/children`, `/api/v1/parent/meetings`

### 3. Common Response Format
```json
{
  "data": {},      // Response data
  "message": "",   // Success/error message
  "status": 200    // HTTP status code
}
```

### 4. Error Handling
```json
{
  "detail": "Error message",
  "code": "ERROR_CODE",
  "status": 400
}
```

## Workflow Documentation

### 1. School Registration Flow
1. SaaS admin creates new tenant
2. School provides registration details
3. System creates school admin account
4. School admin sets up:
   - Academic years
   - Classes and sections
   - Staff accounts
   - Student records

### 2. Parent Onboarding Flow
1. School admin creates student profile
2. System generates parent credentials
3. Parent activates account
4. Parent links to student(s)
5. Parent accesses dashboard

### 3. Academic Management Flow
1. Create academic year
2. Set up classes and sections
3. Assign teachers
4. Create timetables
5. Track attendance
6. Record assessments

### 4. Fee Management Flow
1. Create fee structures
2. Assign to students
3. Generate fee items
4. Process payments
5. Generate receipts

## Common Issues and Solutions

### 1. PostgreSQL Connection Issues
```bash
# Check PostgreSQL service status
# Windows
net start postgresql-x64-15
# Linux
sudo service postgresql status

# Verify database exists
psql -U postgres -l
```

### 2. Redis Connection Issues
```bash
# Check Redis service status
# Windows
net start redis
# Linux
sudo service redis-server status

# Test Redis connection
redis-cli ping
```

### 3. Node.js Issues
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

### 4. Python Environment Issues
```bash
# Recreate virtual environment
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 5. Port Already in Use
```bash
# Find and kill process using port 8000 (backend)
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
# Linux/Mac
lsof -i :8000
kill -9 <PID>

# Find and kill process using port 3000 (frontend)
# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F
# Linux/Mac
lsof -i :3000
kill -9 <PID>
```

## Running Tests

### Backend Tests

```bash
# Navigate to backend directory
cd backend

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Run all tests
pytest

# Run tests with coverage report
pytest --cov=app

# Run specific test file
pytest tests/api/test_auth.py

# Run tests with verbose output
pytest -v

# Run tests and generate HTML coverage report
pytest --cov=app --cov-report=html
```

### Frontend Tests

```bash
# Navigate to project root
cd ..

# Run all tests
npm test

# Run tests in watch mode
npm test -- --watch

# Run tests with coverage
npm test -- --coverage

# Run specific test file
npm test -- src/components/auth/LoginForm.test.tsx

# Update snapshots
npm test -- -u
```

## Development Tools

1. **API Documentation**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

2. **Database Management**
   - pgAdmin: Download from https://www.pgadmin.org/
   - DBeaver: Download from https://dbeaver.io/

3. **Redis Management**
   - Redis Commander: Install with `npm install -g redis-commander`
   - Start with: `redis-commander`
   - Access at: http://localhost:8081

## Troubleshooting

If you encounter any issues:

1. Check the logs:
   - Backend: Look for error messages in the terminal running uvicorn
   - Frontend: Look for error messages in the terminal running npm
   - Database: Check PostgreSQL logs
   - Redis: Check Redis logs

2. Verify services are running:
   - PostgreSQL
   - Redis
   - Backend server
   - Frontend development server

3. Verify environment variables:
   - Backend: Check .env file
   - Frontend: Check .env.local file

4. Check network connectivity:
   - Frontend to Backend
   - Backend to Database
   - Backend to Redis

## Support

If you need help:
1. Check the troubleshooting guide above
2. Review common issues section
3. Check the project documentation
4. Create an issue in the GitHub repository
