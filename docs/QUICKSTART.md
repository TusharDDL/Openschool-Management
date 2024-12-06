# School Management System - Quick Start Guide

This guide will help you get the School Management System up and running quickly for development.

## Quick Setup

### 1. Clone and Setup
```bash
# Clone repository
git clone https://github.com/yourusername/school-management.git
cd school-management

# Install frontend dependencies
npm install

# Setup backend
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
```

### 2. Database Setup
```bash
# Start PostgreSQL
# Create database
createdb school_management

# Run migrations
cd backend
alembic upgrade head

# Create test data
python -m app.scripts.create_test_data
```

### 3. Start Development Servers
```bash
# Terminal 1 - Frontend
npm run dev

# Terminal 2 - Backend
cd backend
uvicorn app.main:app --reload --port 8000
```

## Quick Development Guide

### 1. Adding a New Feature

#### Frontend Component
```typescript
// src/components/features/MyFeature.tsx
'use client';

import { useState } from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';

export function MyFeature() {
  const [data, setData] = useState([]);

  return (
    <Card>
      <h2>My Feature</h2>
      <Button>Click Me</Button>
    </Card>
  );
}
```

#### Backend Endpoint
```python
# backend/app/api/endpoints/my_feature.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import deps

router = APIRouter()

@router.get("/my-feature")
def get_my_feature(db: Session = Depends(deps.get_db)):
    return {"message": "My Feature"}
```

### 2. Common Tasks

#### Adding a Database Model
```python
# backend/app/models/my_model.py
from sqlalchemy import Column, Integer, String
from app.db.base_class import Base

class MyModel(Base):
    __tablename__ = "my_table"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
```

#### Creating a Migration
```bash
# Create migration
alembic revision --autogenerate -m "add my table"

# Apply migration
alembic upgrade head
```

#### Adding an API Service
```typescript
// src/services/myService.ts
import { api } from './api';

export const myService = {
  getData: () => api.get('/my-feature'),
  createData: (data: any) => api.post('/my-feature', data),
};
```

### 3. Testing

#### Frontend Testing
```typescript
// src/components/features/MyFeature.test.tsx
import { render, screen } from '@testing-library/react';
import { MyFeature } from './MyFeature';

describe('MyFeature', () => {
  it('renders correctly', () => {
    render(<MyFeature />);
    expect(screen.getByText('My Feature')).toBeInTheDocument();
  });
});
```

#### Backend Testing
```python
# backend/tests/api/test_my_feature.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_my_feature():
    response = client.get("/api/v1/my-feature")
    assert response.status_code == 200
```

### 4. Common Patterns

#### Protected Route
```typescript
// src/app/(dashboard)/protected/page.tsx
'use client';

import { useAuth } from '@/hooks/useAuth';
import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function ProtectedPage() {
  const { user, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading && !user) {
      router.push('/auth/login');
    }
  }, [user, loading]);

  if (loading) return <div>Loading...</div>;

  return <div>Protected Content</div>;
}
```

#### Form Handling
```typescript
// src/components/forms/MyForm.tsx
'use client';

import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';

const formSchema = z.object({
  name: z.string().min(2),
  email: z.string().email(),
});

export function MyForm() {
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
  });

  const onSubmit = async (data: z.infer<typeof formSchema>) => {
    try {
      // Handle form submission
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <form onSubmit={form.handleSubmit(onSubmit)}>
      {/* Form fields */}
    </form>
  );
}
```

### 5. Debugging

#### Frontend Debugging
```typescript
// Use React Developer Tools
// Add debug logs
const debug = require('debug')('app:myfeature');

function MyComponent() {
  debug('Rendering MyComponent');
  return <div>My Component</div>;
}
```

#### Backend Debugging
```python
# Use debugger
import pdb; pdb.set_trace()

# Or use logging
import logging
logger = logging.getLogger(__name__)

@router.get("/my-endpoint")
async def my_endpoint():
    logger.debug("Processing request")
    return {"message": "success"}
```

### 6. Production Build

#### Frontend Build
```bash
# Build frontend
npm run build

# Test production build
npm run start
```

#### Backend Production
```bash
# Install production dependencies
pip install gunicorn

# Start with gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## Quick Reference

### Environment Variables

#### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_WEBSOCKET_URL=ws://localhost:8000/ws
```

#### Backend (.env)
```env
DATABASE_URL=postgresql://user:pass@localhost:5432/school_management
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key
```

### API Routes

#### Authentication
- POST /api/v1/auth/login
- POST /api/v1/auth/refresh
- POST /api/v1/auth/logout

#### Users
- GET /api/v1/users
- POST /api/v1/users
- GET /api/v1/users/{id}

#### Students
- GET /api/v1/students
- POST /api/v1/students
- GET /api/v1/students/{id}

### Common Commands

```bash
# Frontend
npm run dev        # Start development server
npm run build     # Build for production
npm run lint      # Run linter
npm run test      # Run tests

# Backend
uvicorn app.main:app --reload  # Start development server
pytest                         # Run tests
alembic upgrade head           # Run migrations
```

### Useful Tools

1. Database Management
   - pgAdmin: PostgreSQL GUI
   - DBeaver: Universal database tool

2. API Testing
   - Postman: API testing tool
   - curl: Command-line tool
   - Thunder Client: VS Code extension

3. Development Tools
   - VS Code Extensions:
     - ESLint
     - Prettier
     - Python
     - Thunder Client
     - GitLens

4. Monitoring
   - Prometheus: Metrics collection
   - Grafana: Visualization
   - Sentry: Error tracking