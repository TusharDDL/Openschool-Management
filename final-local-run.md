# Local Development Setup Guide

This guide will help you set up and run the School Management System backend locally.

## Prerequisites

1. Python 3.11 or higher
2. PostgreSQL 15 or higher
3. pip (Python package manager)

## Step 1: Install PostgreSQL

### For Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install -y postgresql postgresql-contrib
```

### For macOS:
```bash
brew install postgresql@15
brew services start postgresql@15
```

### For Windows:
Download and install PostgreSQL from [PostgreSQL Downloads](https://www.postgresql.org/download/windows/)

## Step 2: Configure PostgreSQL

1. Start PostgreSQL service:
```bash
sudo service postgresql start  # For Linux
# or
brew services start postgresql  # For macOS
```

2. Set up the database and user:
```bash
sudo -u postgres psql -c "CREATE DATABASE school_db;"
sudo -u postgres psql -c "ALTER USER postgres WITH PASSWORD 'postgres';"
```

## Step 3: Install Poetry (Python Package Manager)

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Add Poetry to your PATH:
```bash
export PATH="/root/.local/bin:$PATH"  # Linux/macOS
# or
set PATH=%APPDATA%\Python\Scripts;%PATH%  # Windows
```

## Step 4: Clone and Configure the Project

1. Clone the repository (if you haven't already):
```bash
git clone <repository-url>
cd <project-directory>
```

2. Create a .env file in the backend directory:
```bash
cd backend
cp .env.example .env  # If .env.example exists
```

3. Update the .env file with these settings:
```env
# Database settings
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/school_db
ASYNC_DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/school_db

# Security settings
SECRET_KEY=your-secret-key-at-least-32-characters-long
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# First Super Admin
FIRST_SUPERUSER_EMAIL=admin@openhands.com
FIRST_SUPERUSER_PASSWORD=Admin@123
FIRST_SUPERUSER_USERNAME=superadmin
FIRST_SUPERUSER_FULL_NAME="System Administrator"
```

## Step 5: Install Dependencies

```bash
cd backend
poetry install
```

## Step 6: Run Database Migrations

```bash
poetry run alembic upgrade head
```

## Step 7: Start the Backend Server

```bash
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The backend will be available at http://localhost:8000

## Verify the Setup

1. Check if the server is running:
```bash
curl http://localhost:8000/ping
# Should return: {"message":"pong"}
```

2. Access the API documentation:
- OpenAPI (Swagger): http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Default Superuser Credentials

- Email: admin@openhands.com
- Password: Admin@123
- Username: superadmin

## Troubleshooting

### 1. Database Connection Issues

If you get database connection errors:
1. Check if PostgreSQL is running:
```bash
sudo service postgresql status  # Linux
# or
brew services list  # macOS
```

2. Verify database connection settings:
```bash
psql -U postgres -h localhost -d school_db
# Enter the password when prompted (postgres)
```

### 2. Port Already in Use

If port 8000 is already in use:
```bash
# Find the process using port 8000
sudo lsof -i :8000  # Linux/macOS
# or
netstat -ano | findstr :8000  # Windows

# Kill the process
kill -9 <PID>  # Linux/macOS
# or
taskkill /PID <PID> /F  # Windows
```

### 3. Poetry Installation Issues

If Poetry installation fails:
```bash
# Alternative installation method
pip install poetry

# Verify installation
poetry --version
```

### 4. Migration Issues

If you encounter migration errors:
```bash
# Reset migrations
rm -rf backend/alembic/versions/*
poetry run alembic revision --autogenerate -m "Initial migration"
poetry run alembic upgrade head
```

## Development Tips

1. Auto-reload is enabled by default (--reload flag), so the server will restart automatically when you make changes to the code.

2. Check the logs for errors:
```bash
tail -f backend/server.log
```

3. Reset the database if needed:
```bash
sudo -u postgres psql -c "DROP DATABASE school_db;"
sudo -u postgres psql -c "CREATE DATABASE school_db;"
poetry run alembic upgrade head
```

4. Run tests:
```bash
poetry run pytest
```

## Next Steps

1. Access the API documentation at http://localhost:8000/docs
2. Use the default superuser credentials to authenticate
3. Start making API requests to create and manage school data

## Support

If you encounter any issues not covered in this guide, please:
1. Check the project's issue tracker
2. Review the error logs
3. Contact the development team