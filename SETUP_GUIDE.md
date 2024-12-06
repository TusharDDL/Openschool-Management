# School Management System - Complete Setup Guide

This guide provides step-by-step instructions to set up and run the School Management System on your local machine.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [System Requirements](#system-requirements)
3. [Installation Steps](#installation-steps)
4. [Configuration](#configuration)
5. [Running the Application](#running-the-application)
6. [Troubleshooting](#troubleshooting)

## Prerequisites

### Required Software
1. **Node.js**
   ```bash
   # For Ubuntu/Debian
   curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
   sudo apt-get install -y nodejs

   # For Windows
   # Download and install from https://nodejs.org/ (LTS version)

   # Verify installation
   node --version  # Should be 18.x or higher
   npm --version
   ```

2. **Python**
   ```bash
   # For Ubuntu/Debian
   sudo apt update
   sudo apt install python3.11 python3.11-venv python3-pip

   # For Windows
   # Download and install from https://www.python.org/downloads/
   # Make sure to check "Add Python to PATH" during installation

   # Verify installation
   python3 --version  # Should be 3.11 or higher
   pip --version
   ```

3. **PostgreSQL**
   ```bash
   # For Ubuntu/Debian
   sudo apt install postgresql postgresql-contrib

   # For Windows
   # Download and install from https://www.postgresql.org/download/windows/

   # Start PostgreSQL service
   # Ubuntu/Debian
   sudo systemctl start postgresql
   sudo systemctl enable postgresql

   # Windows (PowerShell as Administrator)
   net start postgresql
   ```

4. **Redis**
   ```bash
   # For Ubuntu/Debian
   sudo apt install redis-server
   sudo systemctl start redis-server
   sudo systemctl enable redis-server

   # For Windows
   # Download the Windows Subsystem for Linux (WSL) and install Redis there
   # Or use Docker for Redis
   ```

## System Requirements
- CPU: 2+ cores recommended
- RAM: 4GB minimum, 8GB recommended
- Storage: 10GB free space
- Internet connection for package installation

## Installation Steps

### 1. Clone the Repository
```bash
git clone <your-repository-url>
cd school-management
```

### 2. Frontend Setup

```bash
# Install dependencies
npm install --legacy-peer-deps

# Create environment file
cp .env.example .env.local

# Edit .env.local with these settings:
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_WEBSOCKET_URL=ws://localhost:8000/ws
NEXT_PUBLIC_UPLOAD_URL=http://localhost:8000/uploads
NEXT_PUBLIC_MAX_FILE_SIZE=5242880
```

### 3. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment
python3 -m venv venv

# On Linux/Mac
source venv/bin/activate
# On Windows
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env
```

Edit `.env` with these settings:
```env
# Database settings
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432
POSTGRES_DB=school_management

# JWT Settings
SECRET_KEY=your-secret-key-min-32-chars
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Redis settings
REDIS_URL=redis://localhost:6379/0

# Email settings (optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-specific-password
```

### 4. Database Setup

```bash
# Access PostgreSQL
sudo -u postgres psql

# Create database and user
CREATE DATABASE school_management;
CREATE USER your_username WITH PASSWORD 'your_password';
ALTER ROLE your_username SET client_encoding TO 'utf8';
ALTER ROLE your_username SET default_transaction_isolation TO 'read committed';
ALTER ROLE your_username SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE school_management TO your_username;
\q

# Run migrations
cd backend
alembic upgrade head

# Create initial superuser
python scripts/create_superuser.py
```

## Configuration

### 1. Frontend Configuration (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_WEBSOCKET_URL=ws://localhost:8000/ws
NEXT_PUBLIC_UPLOAD_URL=http://localhost:8000/uploads
NEXT_PUBLIC_MAX_FILE_SIZE=5242880
```

### 2. Backend Configuration (.env)
```env
# Database
DATABASE_URL=postgresql://your_username:your_password@localhost:5432/school_management
ASYNC_DATABASE_URL=postgresql+asyncpg://your_username:your_password@localhost:5432/school_management

# Redis
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=your-secret-key-min-32-chars
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

## Running the Application

### 1. Start Backend Server
```bash
# In backend directory with virtual environment activated
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Start Frontend Development Server
```bash
# In another terminal, from project root
npm run dev
```

The application should now be accessible at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Troubleshooting

### 1. Database Connection Issues
```bash
# Check PostgreSQL service
sudo systemctl status postgresql  # Linux
net start postgresql  # Windows

# Test database connection
psql -U your_username -d school_management -h localhost
```

### 2. Redis Connection Issues
```bash
# Check Redis service
sudo systemctl status redis  # Linux
redis-cli ping  # Should return PONG
```

### 3. Frontend Issues
```bash
# Clear Next.js cache
rm -rf .next
npm run dev

# If module issues
rm -rf node_modules package-lock.json
npm install --legacy-peer-deps
```

### 4. Backend Issues
```bash
# Recreate virtual environment
rm -rf venv
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Reset database
dropdb school_management
createdb school_management
alembic upgrade head
```

### 5. Common Error Messages

1. **"NextRouter was not mounted"**
   - Clear .next directory
   - Restart the development server
   - Make sure you're using client components correctly

2. **"Database connection error"**
   - Verify PostgreSQL is running
   - Check database credentials in .env
   - Ensure database exists

3. **"Redis connection refused"**
   - Verify Redis server is running
   - Check Redis URL in .env

4. **"Module not found"**
   - Run `npm install --legacy-peer-deps`
   - Clear node_modules and reinstall

## Additional Notes

1. **Development Mode**
   - Frontend runs in development mode with hot reloading
   - Backend runs with auto-reload on code changes

2. **Production Mode**
   ```bash
   # Build frontend
   npm run build
   npm start

   # Run backend
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

3. **Database Backups**
   ```bash
   # Backup
   pg_dump -U your_username school_management > backup.sql

   # Restore
   psql -U your_username school_management < backup.sql
   ```

4. **Logs**
   - Frontend logs: Browser console
   - Backend logs: Terminal running uvicorn
   - Database logs: PostgreSQL logs

5. **Security Notes**
   - Change default credentials
   - Use strong passwords
   - Keep environment variables secure
   - Don't commit .env files

For additional help or issues, please refer to:
- Project Documentation: /docs
- GitHub Issues: [Project Issues](https://github.com/yourusername/school-management/issues)
- API Documentation: http://localhost:8000/docs