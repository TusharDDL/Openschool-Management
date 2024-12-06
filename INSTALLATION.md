# School Management System - Installation Guide

This guide provides detailed instructions for setting up the School Management System on your local machine.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Installation Steps](#installation-steps)
3. [Configuration](#configuration)
4. [Running the Application](#running-the-application)
5. [Common Issues](#common-issues)
6. [Feature Documentation](#feature-documentation)

## Prerequisites

### Required Software
1. **Node.js**
   - Version: 18.x or higher
   - Download from: https://nodejs.org/

2. **Python**
   - Version: 3.11 or higher
   - Download from: https://www.python.org/downloads/

3. **PostgreSQL**
   - Version: 15.x
   - Download from: https://www.postgresql.org/download/

4. **Redis**
   - Version: 7.x
   - Windows: https://github.com/microsoftarchive/redis/releases
   - Mac: \`brew install redis\`
   - Linux: \`sudo apt install redis-server\`

5. **Git**
   - Latest version
   - Download from: https://git-scm.com/downloads

### System Requirements
- CPU: 2+ cores recommended
- RAM: 4GB minimum, 8GB recommended
- Storage: 10GB free space
- Internet connection for package installation

## Installation Steps

### 1. Clone the Repository
\`\`\`bash
git clone https://github.com/yourusername/school-management.git
cd school-management
\`\`\`

### 2. Frontend Setup

#### Install Dependencies
\`\`\`bash
# Install npm packages
npm install

# If you encounter any peer dependency issues
npm install --legacy-peer-deps
\`\`\`

#### Environment Setup
\`\`\`bash
# Copy example env file
cp .env.example .env.local

# Edit .env.local with your settings
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_WEBSOCKET_URL=ws://localhost:8000/ws
\`\`\`

### 3. Backend Setup

#### Create Python Virtual Environment
\`\`\`bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
\`\`\`

#### Install Python Dependencies
\`\`\`bash
# Install poetry if not installed
pip install poetry

# Install dependencies
poetry install

# If you don't want to use poetry
pip install -r requirements.txt
\`\`\`

#### Database Setup
\`\`\`bash
# Create PostgreSQL database
createdb school_management

# Copy example env file
cp .env.example .env

# Edit .env with your database credentials
DATABASE_URL=postgresql://username:password@localhost:5432/school_management
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key
\`\`\`

#### Run Migrations
\`\`\`bash
# Apply database migrations
alembic upgrade head

# Create initial superuser
python -m app.scripts.create_superuser
\`\`\`

## Configuration

### 1. Frontend Configuration (.env.local)
\`\`\`env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_WEBSOCKET_URL=ws://localhost:8000/ws
NEXT_PUBLIC_UPLOAD_URL=http://localhost:8000/uploads
NEXT_PUBLIC_MAX_FILE_SIZE=5242880
\`\`\`

### 2. Backend Configuration (.env)
\`\`\`env
# Database
DATABASE_URL=postgresql://username:password@localhost:5432/school_management
ASYNC_DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/school_management

# Redis
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=your-secret-key-at-least-32-characters
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Email (Optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-specific-password

# File Storage (Optional)
UPLOAD_DIR=uploads
MAX_UPLOAD_SIZE=5242880
\`\`\`

## Running the Application

### 1. Development Mode

#### Start Backend Server
\`\`\`bash
# Navigate to backend directory
cd backend

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Start backend server
uvicorn app.main:app --reload --port 8000
\`\`\`

#### Start Frontend Development Server
\`\`\`bash
# In another terminal, from project root
npm run dev
\`\`\`

### 2. Production Mode

#### Build Frontend
\`\`\`bash
# Build frontend
npm run build

# Start production server
npm start
\`\`\`

#### Run Backend with Gunicorn
\`\`\`bash
# Install gunicorn
pip install gunicorn

# Start backend
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
\`\`\`

## Common Issues

### 1. Database Connection Issues
```bash
# Check PostgreSQL service
# Windows
net start postgresql-x64-15
# Linux
sudo service postgresql status

# Create database manually
psql -U postgres
CREATE DATABASE school_management;
```

### 2. Redis Connection Issues
```bash
# Check Redis service
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
poetry install
```

## Feature Documentation

### 1. Multi-tenant System

#### School Onboarding
- Access: Super Admin Portal
- URL: `/dashboard/admin/schools`
- Features:
  - Create new school
  - Configure subdomain
  - Set branding options
  - Create initial admin account

#### Role Management
- Access: School Admin Portal
- URL: `/dashboard/settings/roles`
- Available Roles:
  - Super Admin
  - School Admin
  - Teacher
  - Student
  - Parent

### 2. Academic Management

#### Class Management
- Access: School Admin Portal
- URL: `/dashboard/academics/classes`
- Features:
  - Create/edit classes
  - Manage sections
  - Assign teachers
  - Set subjects

#### Timetable Management
- Access: School Admin & Teacher Portal
- URL: `/dashboard/academics/timetable`
- Features:
  - Create weekly schedule
  - Assign teachers
  - Handle conflicts
  - Generate reports

### 3. Student Management

#### Admission Process
- Access: School Admin Portal
- URL: `/dashboard/students/admission`
- Features:
  - Student registration
  - Document upload
  - Class assignment
  - Fee structure assignment

#### Academic Records
- Access: Teacher Portal
- URL: `/dashboard/students/records`
- Features:
  - Mark attendance
  - Record grades
  - Add remarks
  - Generate reports

### 4. Finance Management

#### Fee Structure
- Access: School Admin Portal
- URL: `/dashboard/finance/structure`
- Features:
  - Create fee types
  - Set amounts
  - Define payment schedule
  - Apply discounts

#### Payment Management
- Access: School Admin Portal
- URL: `/dashboard/finance/payments`
- Features:
  - Record payments
  - Generate receipts
  - Track dues
  - Send reminders

### 5. Communication System

#### Announcements
- Access: All Portals
- URL: `/dashboard/communication`
- Features:
  - Create announcements
  - Target specific groups
  - Schedule messages
  - Track delivery

#### Notifications
- Types:
  - Fee reminders
  - Assignment deadlines
  - Exam schedules
  - General announcements
- Delivery:
  - In-app notifications
  - Email notifications (optional)
  - SMS notifications (optional)

### 6. Reports & Analytics

#### Academic Reports
- Access: School Admin & Teacher Portal
- URL: `/dashboard/reports/academic`
- Types:
  - Performance reports
  - Attendance reports
  - Class-wise analysis
  - Trend analysis

#### Financial Reports
- Access: School Admin Portal
- URL: `/dashboard/reports/finance`
- Types:
  - Collection reports
  - Due reports
  - Discount reports
  - Trend analysis

## Support

For technical support:
1. Check the troubleshooting guide above
2. Review common issues section
3. Contact support team:
   - Email: support@schoolmanagement.com
   - GitHub Issues: [Create new issue](https://github.com/yourusername/school-management/issues)
   - Documentation: [Project Wiki](https://github.com/yourusername/school-management/wiki)