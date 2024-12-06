# Quick Start Guide

## Prerequisites
- Docker and Docker Compose
- Node.js 18+ and npm
- Python 3.10+
- Git

## Local Development Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd School-Management
```

2. **Environment Setup**
```bash
# Copy environment files
cp .env.example .env

# Install frontend dependencies
npm install

# Install backend dependencies (if running without Docker)
cd backend
pip install -r requirements.txt
cd ..
```

3. **Start Backend Services**
```bash
# Start required services using Docker
docker-compose -f docker-compose.local.yml up -d
```

4. **Start Frontend Development Server**
```bash
# In a new terminal
npm run dev
```

5. **Access the Application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/api/v1/docs
- Redis Commander: http://localhost:8081

## Common Issues and Solutions

1. **Database Connection Issues**
- Ensure PostgreSQL is running: `docker-compose -f docker-compose.local.yml ps`
- Check logs: `docker-compose -f docker-compose.local.yml logs db`

2. **Redis Connection Issues**
- Verify Redis is running: `docker-compose -f docker-compose.local.yml ps`
- Check logs: `docker-compose -f docker-compose.local.yml logs redis`

3. **Frontend Build Issues**
- Clear next.js cache: `rm -rf .next`
- Reinstall dependencies: `rm -rf node_modules && npm install`

4. **Backend Issues**
- Check logs: `docker-compose -f docker-compose.local.yml logs backend`
- Rebuild container: `docker-compose -f docker-compose.local.yml build backend`

## Development Workflow

1. **Backend Development**
- API documentation available at: http://localhost:8000/api/v1/docs
- Run tests: `cd backend && pytest`
- Format code: `black .`

2. **Frontend Development**
- Run linter: `npm run lint`
- Build production: `npm run build`

## Stopping the Application
```bash
# Stop all services
docker-compose -f docker-compose.local.yml down

# To remove volumes as well
docker-compose -f docker-compose.local.yml down -v
```