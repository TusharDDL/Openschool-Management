# School Management System - Development Guide

This guide provides detailed information for developers who want to extend or modify the School Management System.

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Development Setup](#development-setup)
3. [Code Structure](#code-structure)
4. [Adding New Features](#adding-new-features)
5. [Testing Guidelines](#testing-guidelines)
6. [Deployment Process](#deployment-process)

## Architecture Overview

### Frontend Architecture
```
src/
├── app/                    # Next.js pages and routing
│   ├── (dashboard)/       # Dashboard routes
│   ├── auth/              # Authentication routes
│   └── layout.tsx         # Root layout
├── components/            # React components
│   ├── ui/               # Reusable UI components
│   ├── layout/           # Layout components
│   ├── forms/            # Form components
│   └── features/         # Feature-specific components
├── services/             # API integration
├── hooks/                # Custom React hooks
├── contexts/             # React contexts
├── lib/                  # Utility functions
└── types/                # TypeScript types
```

### Backend Architecture
```
backend/
├── app/
│   ├── api/              # API routes
│   ├── core/             # Core functionality
│   ├── models/           # Database models
│   ├── schemas/          # Pydantic schemas
│   ├── services/         # Business logic
│   └── utils/            # Utility functions
├── tests/                # Test files
└── alembic/              # Database migrations
```

## Development Setup

### Frontend Development

#### 1. Component Development
```typescript
// src/components/features/MyFeature.tsx
import { useState } from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';

export function MyFeature() {
  const [data, setData] = useState([]);

  return (
    <Card>
      {/* Component content */}
    </Card>
  );
}
```

#### 2. API Integration
```typescript
// src/services/myService.ts
import { api } from './api';

export interface MyData {
  id: number;
  name: string;
}

class MyService {
  async getData(): Promise<MyData[]> {
    const response = await api.get('/endpoint');
    return response.data;
  }

  async createData(data: Omit<MyData, 'id'>): Promise<MyData> {
    const response = await api.post('/endpoint', data);
    return response.data;
  }
}

export const myService = new MyService();
```

#### 3. Form Handling
```typescript
// src/components/forms/MyForm.tsx
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

  return (
    <form onSubmit={form.handleSubmit(onSubmit)}>
      {/* Form fields */}
    </form>
  );
}
```

### Backend Development

#### 1. Model Creation
```python
# backend/app/models/my_model.py
from sqlalchemy import Column, Integer, String
from app.db.base_class import Base

class MyModel(Base):
    __tablename__ = "my_table"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
```

#### 2. Schema Definition
```python
# backend/app/schemas/my_schema.py
from pydantic import BaseModel

class MySchemaBase(BaseModel):
    name: str
    description: str | None = None

class MySchemaCreate(MySchemaBase):
    pass

class MySchema(MySchemaBase):
    id: int

    class Config:
        from_attributes = True
```

#### 3. API Route Creation
```python
# backend/app/api/endpoints/my_endpoint.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas import MySchema, MySchemaCreate
from app.services import my_service

router = APIRouter()

@router.get("/", response_model=list[MySchema])
def get_items(db: Session = Depends(deps.get_db)):
    return my_service.get_items(db)

@router.post("/", response_model=MySchema)
def create_item(item: MySchemaCreate, db: Session = Depends(deps.get_db)):
    return my_service.create_item(db, item)
```

## Adding New Features

### 1. Frontend Feature Addition

#### Create Components
```typescript
// src/components/features/NewFeature/
├── NewFeature.tsx         # Main component
├── NewFeatureForm.tsx     # Form component
├── NewFeatureList.tsx     # List component
└── NewFeatureCard.tsx     # Card component
```

#### Add Route
```typescript
// src/app/(dashboard)/new-feature/page.tsx
import { NewFeature } from '@/components/features/NewFeature';

export default function NewFeaturePage() {
  return <NewFeature />;
}
```

#### Add Navigation
```typescript
// src/components/layout/Sidebar.tsx
const menuItems = [
  // ...existing items
  {
    icon: Icon,
    label: 'New Feature',
    href: '/dashboard/new-feature',
  },
];
```

### 2. Backend Feature Addition

#### Create Model
```python
# backend/app/models/new_feature.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class NewFeature(Base):
    __tablename__ = "new_features"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="new_features")
```

#### Create Schema
```python
# backend/app/schemas/new_feature.py
from pydantic import BaseModel

class NewFeatureBase(BaseModel):
    name: str

class NewFeatureCreate(NewFeatureBase):
    pass

class NewFeature(NewFeatureBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
```

#### Add Service
```python
# backend/app/services/new_feature.py
from sqlalchemy.orm import Session
from app.models import NewFeature
from app.schemas.new_feature import NewFeatureCreate

class NewFeatureService:
    def create(self, db: Session, data: NewFeatureCreate, user_id: int):
        db_obj = NewFeature(**data.model_dump(), user_id=user_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

new_feature_service = NewFeatureService()
```

## Testing Guidelines

### Frontend Testing

#### Component Testing
```typescript
// src/components/features/NewFeature/NewFeature.test.tsx
import { render, screen } from '@testing-library/react';
import { NewFeature } from './NewFeature';

describe('NewFeature', () => {
  it('renders correctly', () => {
    render(<NewFeature />);
    expect(screen.getByText('New Feature')).toBeInTheDocument();
  });
});
```

#### API Testing
```typescript
// src/services/__tests__/newFeatureService.test.ts
import { newFeatureService } from '../newFeatureService';

describe('newFeatureService', () => {
  it('fetches data correctly', async () => {
    const data = await newFeatureService.getData();
    expect(data).toBeDefined();
  });
});
```

### Backend Testing

#### API Testing
```python
# backend/tests/api/test_new_feature.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_new_feature():
    response = client.post(
        "/api/v1/new-features/",
        json={"name": "Test Feature"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Test Feature"
```

#### Service Testing
```python
# backend/tests/services/test_new_feature.py
import pytest
from app.services.new_feature import new_feature_service

def test_create_new_feature(db_session):
    feature = new_feature_service.create(
        db_session,
        NewFeatureCreate(name="Test"),
        user_id=1
    )
    assert feature.name == "Test"
```

## Deployment Process

### 1. Build Process
```bash
# Frontend build
npm run build

# Backend build
poetry build
```

### 2. Database Migration
```bash
# Create migration
alembic revision --autogenerate -m "Add new feature"

# Apply migration
alembic upgrade head
```

### 3. Environment Configuration
```bash
# Production environment variables
NEXT_PUBLIC_API_URL=https://api.example.com
DATABASE_URL=postgresql://user:pass@host:5432/db
REDIS_URL=redis://host:6379/0
```

### 4. Monitoring Setup
```python
# backend/app/core/monitoring.py
from prometheus_client import Counter, Histogram

http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

request_duration_seconds = Histogram(
    'request_duration_seconds',
    'Request duration in seconds',
    ['method', 'endpoint']
)
```

## Best Practices

### 1. Code Style
- Follow ESLint/Prettier configuration
- Use TypeScript strictly
- Follow PEP 8 for Python code
- Write meaningful commit messages

### 2. Security
- Validate all inputs
- Use proper authentication
- Implement rate limiting
- Handle sensitive data carefully

### 3. Performance
- Optimize database queries
- Implement caching
- Use proper indexing
- Monitor resource usage

### 4. Documentation
- Document all APIs
- Write clear component documentation
- Maintain changelog
- Update installation guides