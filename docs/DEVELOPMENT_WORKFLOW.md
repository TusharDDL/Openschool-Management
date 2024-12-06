# Development Workflow Guide

## Getting Started

1. **Clone and Setup**
```bash
git clone <repository-url>
cd school-management
./setup.sh
```

2. **Start Development Servers**
```bash
# Terminal 1 - Backend
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2 - Frontend
npm run dev
```

## Development Process

### 1. Creating New Features

1. **Create a Feature Branch**
```bash
git checkout -b feature/feature-name
```

2. **Follow Feature Implementation Steps**
   - Create necessary database migrations
   - Implement backend endpoints
   - Add frontend components
   - Write tests
   - Update documentation

3. **Testing Locally**
   - Run backend tests: `pytest`
   - Run frontend tests: `npm test`
   - Manual testing in browser

4. **Create Pull Request**
   - Push changes
   - Create PR with description
   - Request review

### 2. Code Organization

1. **Backend Structure**
```
backend/
├── app/
│   ├── api/          # API endpoints
│   ├── core/         # Core functionality
│   ├── models/       # Database models
│   └── schemas/      # Pydantic schemas
├── migrations/       # Database migrations
└── tests/           # Test files
```

2. **Frontend Structure**
```
src/
├── app/             # Next.js pages
├── components/      # React components
├── hooks/           # Custom hooks
├── providers/       # Context providers
├── services/        # API services
└── types/          # TypeScript types
```

### 3. Database Changes

1. **Create Migration**
```bash
cd backend
alembic revision --autogenerate -m "description"
```

2. **Apply Migration**
```bash
alembic upgrade head
```

3. **Rollback if Needed**
```bash
alembic downgrade -1
```

### 4. Testing

1. **Backend Tests**
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_auth.py

# Run with coverage
pytest --cov=app
```

2. **Frontend Tests**
```bash
# Run all tests
npm test

# Run specific test
npm test -- Button.test.tsx

# Update snapshots
npm test -- -u
```

### 5. Code Quality

1. **Linting**
```bash
# Backend
flake8 app tests

# Frontend
npm run lint
```

2. **Type Checking**
```bash
# Frontend
npm run type-check
```

3. **Formatting**
```bash
# Backend
black app tests

# Frontend
npm run format
```

### 6. Deployment

1. **Staging Deployment**
```bash
# Build frontend
npm run build

# Start services
docker-compose -f docker-compose.staging.yml up -d
```

2. **Production Deployment**
```bash
# Build frontend
npm run build

# Start services
docker-compose -f docker-compose.prod.yml up -d
```

## Best Practices

### 1. Git Commits

- Use descriptive commit messages
- Follow conventional commits format
- Keep commits focused and atomic

### 2. Code Review

- Review your own code first
- Write descriptive PR descriptions
- Address all review comments
- Keep PRs manageable in size

### 3. Documentation

- Update README when needed
- Document new features
- Add JSDoc comments
- Update API documentation

### 4. Testing

- Write tests for new features
- Maintain test coverage
- Test edge cases
- Add integration tests

### 5. Performance

- Profile slow operations
- Optimize database queries
- Use proper caching
- Monitor memory usage

## Troubleshooting

### 1. Database Issues
```bash
# Reset database
dropdb school_management
createdb school_management
alembic upgrade head
```

### 2. Frontend Issues
```bash
# Clear Next.js cache
rm -rf .next
npm run dev
```

### 3. Backend Issues
```bash
# Recreate virtual environment
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Additional Resources

1. **Documentation**
   - [FastAPI Docs](https://fastapi.tiangolo.com/)
   - [Next.js Docs](https://nextjs.org/docs)
   - [TypeScript Docs](https://www.typescriptlang.org/docs)

2. **Tools**
   - [PostgreSQL Docs](https://www.postgresql.org/docs/)
   - [Redis Docs](https://redis.io/documentation)
   - [Docker Docs](https://docs.docker.com/)