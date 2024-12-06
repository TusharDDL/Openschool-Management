# Developer Guide - School Management System

This guide helps developers understand the codebase and set up their development environment.

## Project Structure

```
school-management/
├── src/                    # Frontend source code
│   ├── app/               # Next.js pages and routing
│   ├── components/        # React components
│   ├── services/          # API integration
│   ├── contexts/          # React contexts
│   ├── hooks/             # Custom React hooks
│   └── types/             # TypeScript types
├── backend/               # Backend source code
│   ├── app/              # Main application
│   │   ├── api/          # API routes
│   │   ├── core/         # Core functionality
│   │   ├── models/       # Database models
│   │   ├── schemas/      # Pydantic schemas
│   │   └── services/     # Business logic
│   └── tests/            # Backend tests
├── docs/                 # Documentation
└── docker/               # Docker configurations
```

## Tech Stack

### Frontend
- Next.js 15.0
- React 19
- TypeScript
- TailwindCSS
- Radix UI Components

### Backend
- FastAPI
- PostgreSQL
- Redis
- SQLAlchemy

## Development Setup

### Prerequisites
1. Install required software:
   - Node.js 18+
   - Python 3.11+
   - Docker and Docker Compose
   - PostgreSQL 15+
   - Redis 7+

### Frontend Development

1. Install dependencies:
```bash
npm install
```

2. Start development server:
```bash
npm run dev
```

3. Key folders:
- `src/components`: Reusable UI components
- `src/app`: Pages and routing
- `src/services`: API integration
- `src/contexts`: State management

### Backend Development

1. Install dependencies:
```bash
cd backend
poetry install
```

2. Start development server:
```bash
poetry run uvicorn app.main:app --reload
```

3. Key folders:
- `app/api`: API routes
- `app/models`: Database models
- `app/schemas`: Pydantic schemas
- `app/services`: Business logic

## API Integration

### Authentication
```typescript
// Login
const response = await authAPI.login(email, password);

// Logout
await authAPI.logout();
```

### Student Management
```typescript
// Get all students
const students = await studentAPI.getAll();

// Create student
const newStudent = await studentAPI.create(studentData);
```

### Academic Management
```typescript
// Get timetable
const timetable = await academicAPI.getTimetable(classId);

// Submit attendance
await academicAPI.submitAttendance(attendanceData);
```

## Common Development Tasks

### Adding a New Feature

1. Backend:
   - Add models in `backend/app/models`
   - Create schemas in `backend/app/schemas`
   - Add API routes in `backend/app/api`
   - Implement business logic in `backend/app/services`

2. Frontend:
   - Add API service in `src/services`
   - Create components in `src/components`
   - Add pages in `src/app`
   - Update types in `src/types`

### Database Migrations

1. Create migration:
```bash
alembic revision --autogenerate -m "description"
```

2. Apply migration:
```bash
alembic upgrade head
```

### Running Tests

1. Backend tests:
```bash
cd backend
poetry run pytest
```

2. Frontend tests:
```bash
npm run test
```

## Code Style Guide

### TypeScript/React
- Use functional components
- Implement proper error handling
- Use TypeScript types
- Follow React hooks best practices

### Python/FastAPI
- Use type hints
- Follow PEP 8
- Implement proper error handling
- Use dependency injection

## Deployment

### Development
```bash
docker-compose up --build
```

### Production
1. Build images:
```bash
docker-compose -f docker-compose.prod.yml build
```

2. Deploy:
```bash
docker-compose -f docker-compose.prod.yml up -d
```

## Troubleshooting

### Common Issues

1. Database Connection:
```bash
# Check PostgreSQL
docker-compose exec db psql -U postgres
```

2. Redis Connection:
```bash
# Check Redis
docker-compose exec redis redis-cli ping
```

3. Backend Logs:
```bash
docker-compose logs backend
```

### Getting Help
- Check issue tracker
- Review documentation
- Contact senior developers

## Best Practices

1. Code Quality
   - Write tests
   - Use TypeScript/Python type hints
   - Follow coding standards
   - Document complex logic

2. Git Workflow
   - Create feature branches
   - Write clear commit messages
   - Review code before merging
   - Keep branches up to date

3. Security
   - Validate inputs
   - Use proper authentication
   - Handle sensitive data carefully
   - Follow security best practices