# School Management System - Troubleshooting Guide

## Table of Contents
1. [Installation Issues](#installation-issues)
2. [Frontend Issues](#frontend-issues)
3. [Backend Issues](#backend-issues)
4. [Database Issues](#database-issues)
5. [Authentication Issues](#authentication-issues)
6. [Performance Issues](#performance-issues)
7. [Common Error Messages](#common-error-messages)

## Installation Issues

### Node.js Installation

#### Error: Node.js version not compatible
```bash
Error: The engine "node" is incompatible with this module
```

Solution:
1. Install nvm (Node Version Manager):
```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
```

2. Install correct Node.js version:
```bash
nvm install 18
nvm use 18
```

### Python Environment

#### Error: Poetry installation fails
```bash
ERROR: Poetry installation failed
```

Solution:
1. Install Python 3.11 first:
```bash
# Ubuntu/Debian
sudo apt install python3.11 python3.11-venv

# macOS
brew install python@3.11
```

2. Install Poetry using pip:
```bash
pip install poetry
```

### Database Setup

#### Error: PostgreSQL connection failed
```bash
Error: Connection to database failed
```

Solution:
1. Check PostgreSQL service:
```bash
# Ubuntu/Debian
sudo service postgresql status

# macOS
brew services list | grep postgresql
```

2. Create database manually:
```bash
sudo -u postgres psql
CREATE DATABASE school_management;
CREATE USER myuser WITH PASSWORD 'mypassword';
GRANT ALL PRIVILEGES ON DATABASE school_management TO myuser;
```

## Frontend Issues

### Build Errors

#### Error: Module not found
```bash
Error: Cannot find module '@/components/ui/button'
```

Solution:
1. Check tsconfig.json paths:
```json
{
  "compilerOptions": {
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

2. Clear build cache:
```bash
rm -rf .next
npm run build
```

### Runtime Errors

#### Error: Hydration failed
```
Warning: Hydration failed because the initial UI does not match what was rendered on the server
```

Solution:
1. Check for useEffect usage:
```typescript
// Wrong
const [isClient, setIsClient] = useState(true);

// Correct
const [isClient, setIsClient] = useState(false);
useEffect(() => {
  setIsClient(true);
}, []);
```

2. Use dynamic imports for client components:
```typescript
import dynamic from 'next/dynamic';

const ClientComponent = dynamic(() => import('./ClientComponent'), {
  ssr: false
});
```

## Backend Issues

### API Errors

#### Error: CORS issues
```
Access to fetch at 'http://localhost:8000' from origin 'http://localhost:3000' has been blocked by CORS policy
```

Solution:
1. Update CORS settings in backend/app/main.py:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Database Migration Issues

#### Error: Alembic migration conflicts
```
ERROR [alembic.runtime.migration] Can't locate revision identified by '1234abc'
```

Solution:
1. Reset migrations:
```bash
# Delete migration files
rm -rf migrations/versions/*

# Create fresh migration
alembic revision --autogenerate -m "fresh_start"
alembic upgrade head
```

## Database Issues

### Connection Issues

#### Error: Too many connections
```
FATAL: remaining connection slots are reserved for non-replication superuser connections
```

Solution:
1. Update PostgreSQL configuration:
```bash
# Edit postgresql.conf
max_connections = 200
```

2. Implement connection pooling:
```python
# backend/app/db/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=20,
    max_overflow=0
)
```

### Performance Issues

#### Slow Queries
```
Query took too long to execute
```

Solution:
1. Add indexes:
```sql
CREATE INDEX idx_student_class ON students(class_id);
CREATE INDEX idx_payment_date ON payments(payment_date);
```

2. Optimize queries:
```python
# Instead of
db.query(Student).all()

# Use specific columns
db.query(Student.id, Student.name).all()
```

## Authentication Issues

### Token Issues

#### Error: Token expired
```
JWT token has expired
```

Solution:
1. Implement token refresh:
```typescript
// frontend/src/services/api.ts
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      try {
        const newToken = await refreshToken();
        error.config.headers['Authorization'] = `Bearer ${newToken}`;
        return api.request(error.config);
      } catch (refreshError) {
        // Redirect to login
        window.location.href = '/auth/login';
      }
    }
    return Promise.reject(error);
  }
);
```

### Login Issues

#### Error: Invalid credentials
```
Authentication failed: Invalid email or password
```

Solution:
1. Implement password reset:
```python
@router.post("/auth/reset-password")
async def reset_password(email: str):
    user = await get_user_by_email(email)
    if user:
        token = create_reset_token(user.id)
        await send_reset_email(user.email, token)
    return {"message": "If email exists, reset instructions have been sent"}
```

## Performance Issues

### Slow Page Load

#### Issue: Large bundle size
Solution:
1. Implement code splitting:
```typescript
// Use dynamic imports
const HeavyComponent = dynamic(() => import('./HeavyComponent'), {
  loading: () => <LoadingSpinner />
});
```

2. Optimize images:
```typescript
import Image from 'next/image';

export function OptimizedImage() {
  return (
    <Image
      src="/large-image.jpg"
      width={800}
      height={600}
      placeholder="blur"
      loading="lazy"
    />
  );
}
```

### Memory Leaks

#### Issue: Component memory leak
Solution:
1. Clean up useEffect:
```typescript
useEffect(() => {
  const subscription = someAPI.subscribe();
  
  return () => {
    subscription.unsubscribe();
  };
}, []);
```

## Common Error Messages

### 1. "Invalid token signature"
Cause: JWT token has been tampered with or is invalid
Solution:
```typescript
// Check token format
const token = localStorage.getItem('token');
if (token && token.split('.').length !== 3) {
  // Invalid token format
  localStorage.removeItem('token');
  window.location.href = '/auth/login';
}
```

### 2. "Database connection error"
Cause: Database is not running or connection parameters are incorrect
Solution:
```bash
# Check database status
sudo service postgresql status

# Check connection parameters
psql -h localhost -U myuser -d school_management
```

### 3. "File upload failed"
Cause: File size exceeds limit or invalid file type
Solution:
```typescript
// Implement file validation
const validateFile = (file: File) => {
  const maxSize = 5 * 1024 * 1024; // 5MB
  const allowedTypes = ['image/jpeg', 'image/png', 'application/pdf'];
  
  if (file.size > maxSize) {
    throw new Error('File size exceeds 5MB limit');
  }
  
  if (!allowedTypes.includes(file.type)) {
    throw new Error('Invalid file type');
  }
};
```

## Monitoring and Debugging

### 1. Frontend Monitoring
```typescript
// Implement error boundary
class ErrorBoundary extends React.Component {
  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    // Log error to monitoring service
    logError(error, errorInfo);
  }
  
  render() {
    return this.props.children;
  }
}
```

### 2. Backend Monitoring
```python
# Implement request logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    
    logger.info(
        f"Path: {request.url.path} "
        f"Duration: {duration:.2f}s "
        f"Status: {response.status_code}"
    )
    return response
```

### 3. Database Monitoring
```python
# Monitor query performance
from sqlalchemy import event

@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    conn.info.setdefault('query_start_time', []).append(time.time())

@event.listens_for(Engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    total = time.time() - conn.info['query_start_time'].pop()
    if total > 0.5:  # Log slow queries (>500ms)
        logger.warning(f"Slow Query: {statement} took {total:.2f}s")
```