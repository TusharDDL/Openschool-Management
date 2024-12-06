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
sudo -u postgres psql

# In PostgreSQL prompt:
CREATE USER school_user WITH PASSWORD 'school_password' SUPERUSER;
CREATE DATABASE school_management;
GRANT ALL PRIVILEGES ON DATABASE school_management TO school_user;
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

# File Storage
UPLOAD_DIR=uploads
MAX_UPLOAD_SIZE=5242880
EOL

# Run database migrations
PYTHONPATH=/path/to/your/backend alembic upgrade head

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
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_WEBSOCKET_URL=ws://localhost:8000/ws
NEXT_PUBLIC_UPLOAD_URL=http://localhost:8000/uploads
NEXT_PUBLIC_MAX_FILE_SIZE=5242880
EOL

# Start frontend development server
npm run dev
```

## Accessing the Application

1. Frontend: http://localhost:3000
2. Backend API: http://localhost:8000
3. API Documentation: http://localhost:8000/docs
4. Admin Dashboard: http://localhost:3000/dashboard/admin

## Default Credentials

The system will create a default superuser with the following credentials:
- Email: admin@example.com
- Password: admin123

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