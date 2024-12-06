#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}School Management System Setup Script${NC}"
echo "======================================"

# Check prerequisites
echo -e "\n${YELLOW}Checking prerequisites...${NC}"

# Check Node.js
if ! command -v node &> /dev/null; then
    echo -e "${RED}Node.js is not installed. Please install Node.js 18.x or higher${NC}"
    exit 1
fi

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python 3 is not installed. Please install Python 3.11 or higher${NC}"
    exit 1
fi

# Check PostgreSQL
if ! command -v psql &> /dev/null; then
    echo -e "${RED}PostgreSQL is not installed. Please install PostgreSQL 15.x${NC}"
    exit 1
fi

# Check Redis
if ! command -v redis-cli &> /dev/null; then
    echo -e "${RED}Redis is not installed. Please install Redis${NC}"
    exit 1
fi

echo -e "${GREEN}All prerequisites are installed!${NC}"

# Frontend setup
echo -e "\n${YELLOW}Setting up frontend...${NC}"
npm install --legacy-peer-deps

if [ ! -f .env.local ]; then
    echo "Creating .env.local file..."
    cat > .env.local << EOL
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_WEBSOCKET_URL=ws://localhost:8000/ws
NEXT_PUBLIC_UPLOAD_URL=http://localhost:8000/uploads
NEXT_PUBLIC_MAX_FILE_SIZE=5242880
EOL
    echo -e "${GREEN}Created .env.local file${NC}"
fi

# Backend setup
echo -e "\n${YELLOW}Setting up backend...${NC}"
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating backend .env file..."
    cat > .env << EOL
# Database settings
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432
POSTGRES_DB=school_management

# JWT Settings
SECRET_KEY=your-super-secret-key-min-32-chars-long
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Redis settings
REDIS_URL=redis://localhost:6379/0
EOL
    echo -e "${GREEN}Created backend .env file${NC}"
fi

# Database setup
echo -e "\n${YELLOW}Setting up database...${NC}"

# Create database if it doesn't exist
PGPASSWORD=postgres psql -U postgres -h localhost -tc "SELECT 1 FROM pg_database WHERE datname = 'school_management'" | grep -q 1 || PGPASSWORD=postgres psql -U postgres -h localhost -c "CREATE DATABASE school_management"

# Run migrations
echo "Running database migrations..."
alembic upgrade head

echo -e "\n${GREEN}Setup completed successfully!${NC}"
echo -e "\nTo start the application:"
echo -e "${YELLOW}1. Start backend:${NC}"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
echo -e "\n${YELLOW}2. In another terminal, start frontend:${NC}"
echo "   npm run dev"
echo -e "\n${GREEN}The application will be available at:${NC}"
echo "Frontend: http://localhost:3000"
echo "Backend API: http://localhost:8000"
echo "API Documentation: http://localhost:8000/docs"