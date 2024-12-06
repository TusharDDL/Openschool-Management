# School Management System - Code Structure Documentation

## Frontend Structure

### Core Files

1. **Root Layout** (`src/app/layout.tsx`)
```typescript
// Root layout component that wraps all pages
// Provides authentication and global UI elements
export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <AuthProvider>{children}</AuthProvider>
      </body>
    </html>
  );
}
```

2. **Auth Provider** (`src/providers/auth-provider.tsx`)
```typescript
// Authentication provider component
// Manages auth state and operations
export function AuthProvider({ children }: { children: React.ReactNode }) {
  // Auth state management
  const [user, setUser] = useState<User | null>(null);
  // Auth operations: login, logout, etc.
}
```

3. **API Service** (`src/services/api.ts`)
```typescript
// API service configuration and endpoints
// Handles all API requests with axios
const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  // ... configuration
});
```

### Page Components

1. **Home Page** (`src/app/page.tsx`)
```typescript
// Home page component
// Handles initial routing based on auth state
export default function Home() {
  // Routing logic
}
```

2. **Login Page** (`src/app/(auth)/login/page.tsx`)
```typescript
// Login page component
// Handles user authentication
export default function LoginPage() {
  // Login form and submission
}
```

3. **Dashboard** (`src/app/dashboard/page.tsx`)
```typescript
// Dashboard main page
// Protected route for authenticated users
export default function DashboardPage() {
  // Dashboard content
}
```

## Backend Structure

### Core Files

1. **Main Application** (`backend/app/main.py`)
```python
# Main FastAPI application entry point
# Configures middleware, routes, and error handlers
app = FastAPI(
    title=settings.PROJECT_NAME,
    # ... configuration
)
```

2. **Database Configuration** (`backend/app/core/database.py`)
```python
# Database configuration and session management
# SQLAlchemy setup and connection handling
from sqlalchemy import create_engine
# ... database setup
```

3. **Authentication** (`backend/app/core/auth.py`)
```python
# Authentication logic
# JWT token handling and user verification
from jose import JWTError, jwt
# ... auth functions
```

### API Endpoints

1. **API Router** (`backend/app/api/v1/api.py`)
```python
# Main API router
# Combines all endpoint routers
from fastapi import APIRouter
# ... route configuration
```

2. **Auth Endpoints** (`backend/app/api/v1/endpoints/auth.py`)
```python
# Authentication endpoints
# Login, register, and token management
@router.post("/login")
async def login(
    # ... login endpoint
)
```

3. **Student Endpoints** (`backend/app/api/v1/endpoints/students.py`)
```python
# Student management endpoints
# CRUD operations for students
@router.get("/students")
async def get_students(
    # ... student endpoints
)
```

## Key Configuration Files

1. **Frontend Environment** (`.env.local`)
```env
# Frontend environment variables
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_WEBSOCKET_URL=ws://localhost:8000/ws
```

2. **Backend Environment** (`backend/.env`)
```env
# Backend environment variables
DATABASE_URL=postgresql://user:pass@localhost:5432/db
SECRET_KEY=your-secret-key
```

3. **Package Configuration** (`package.json`)
```json
{
  "name": "school-management",
  "version": "0.1.0",
  // ... dependencies and scripts
}
```

## Directory Structure Explanation

### Frontend (`/src`)
- `app/`: Next.js 13+ app directory
  - `(auth)/`: Authentication-related pages
  - `dashboard/`: Dashboard and protected pages
- `components/`: Reusable React components
- `providers/`: Context providers
- `services/`: API and other services
- `types/`: TypeScript type definitions

### Backend (`/backend`)
- `app/`: Main application code
  - `api/`: API endpoints and routers
  - `core/`: Core functionality
  - `models/`: Database models
- `migrations/`: Database migrations
- `tests/`: Test files

### Shared
- `docs/`: Project documentation
- `public/`: Static files
- Configuration files in root directory

## File Naming Conventions

1. **Frontend**
- React Components: PascalCase (e.g., `AuthProvider.tsx`)
- Utilities/Services: camelCase (e.g., `api.ts`)
- Pages: page.tsx in corresponding directories

2. **Backend**
- Python modules: snake_case (e.g., `database.py`)
- API endpoints: snake_case (e.g., `auth_router.py`)

## Import Conventions

1. **Frontend**
```typescript
// Absolute imports from src
import { something } from '@/components/...'
// External packages
import { useState } from 'react'
```

2. **Backend**
```python
# Standard library imports
from typing import Optional
# Third-party imports
from fastapi import FastAPI
# Local imports
from app.core import config
```

## Best Practices

1. **Frontend**
- Use 'use client' directive for client components
- Keep components small and focused
- Use TypeScript for type safety
- Implement proper error boundaries

2. **Backend**
- Follow FastAPI best practices
- Implement proper error handling
- Use dependency injection
- Keep routes organized and documented

## Testing Structure

1. **Frontend Tests** (`src/__tests__/`)
- Component tests
- Integration tests
- API mocks

2. **Backend Tests** (`backend/tests/`)
- API endpoint tests
- Unit tests
- Integration tests