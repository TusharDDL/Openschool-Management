# School Management SaaS Platform (MVP)

A streamlined School Management System with multi-tenant architecture, offering essential features for school administration, student management, and academic operations.

## Core Features

### 1. Multi-tenant System
- School-specific subdomain (e.g., school1.domain.com)
- Isolated data per school
- Basic school branding (logo, colors)
- Role-based access control

### 2. Portal Access
- **SaaS Admin Portal**
  - School onboarding
  - Tenant management
  - System monitoring
- **School Admin Portal**
  - Student management
  - Staff management
  - Academic operations
  - Fee management
- **Student/Parent Portal**
  - Profile view
  - Academic performance
  - Fee status
  - Announcements

### 3. Key Functionalities

#### Academic Management
- Class/Section management
- Basic timetable creation
- Attendance tracking
- Exam results management

#### Student Management
- Student registration
- Profile management
- Attendance records
- Academic history

#### Fee Management
- Fee structure setup
- Fee allocation
- Due date management
- Payment status tracking

#### Communication
- School announcements
- Class-specific notices
- Basic notification system

## Technical Stack

### Frontend
- Next.js 15.0
- React 19
- TypeScript
- TailwindCSS
- Radix UI Components

### Backend
- FastAPI (Python 3.11+)
- PostgreSQL 15+
- Redis for caching
- JWT authentication

### Infrastructure
- Docker containerization
- Nginx reverse proxy
- Basic monitoring

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Node.js 18+
- Python 3.11+

### Installation

1. Clone the repository:
\`\`\`bash
git clone https://github.com/yourusername/school-management.git
cd school-management
\`\`\`

2. Environment setup:
\`\`\`bash
cp .env.example .env
# Edit .env with your configurations
\`\`\`

3. Start services:
\`\`\`bash
docker-compose up --build
\`\`\`

4. Initialize database:
\`\`\`bash
docker-compose exec backend alembic upgrade head
docker-compose exec backend python -m app.scripts.create_superuser
\`\`\`

## Portal Access Guide

### 1. SaaS Admin Portal
- URL: https://admin.yourdomain.com
- Default credentials:
  - Email: admin@schoolsaas.com
  - Password: (set during superuser creation)

Features:
- School onboarding
- Tenant management
- System monitoring
- Support management

### 2. School Admin Portal
- URL: https://[school-subdomain].yourdomain.com/admin
- Credentials: Created by SaaS admin

Features:
- Dashboard
- Student management
- Staff management
- Academic operations
- Fee management
- Communication center

### 3. Student/Parent Portal
- URL: https://[school-subdomain].yourdomain.com
- Credentials: Provided by school admin

Features:
- Profile management
- Academic performance
- Attendance records
- Fee status
- Announcements

## API Documentation

### Authentication
\`\`\`bash
POST /api/v1/auth/login
POST /api/v1/auth/refresh-token
POST /api/v1/auth/logout
\`\`\`

### Student Management
\`\`\`bash
GET /api/v1/students
POST /api/v1/students
GET /api/v1/students/{id}
PUT /api/v1/students/{id}
DELETE /api/v1/students/{id}
\`\`\`

### Academic Management
\`\`\`bash
GET /api/v1/academic/classes
POST /api/v1/academic/classes
GET /api/v1/academic/timetable
POST /api/v1/academic/attendance
GET /api/v1/academic/results
\`\`\`

### Fee Management
\`\`\`bash
GET /api/v1/fees/structure
POST /api/v1/fees/structure
GET /api/v1/fees/student/{id}
POST /api/v1/fees/allocate
\`\`\`

## Development Guide

### Frontend Development
\`\`\`bash
cd frontend
npm install
npm run dev
\`\`\`

Key directories:
- /src/components - Reusable UI components
- /src/app - Pages and routing
- /src/services - API integration
- /src/contexts - State management
- /src/hooks - Custom hooks

### Backend Development
\`\`\`bash
cd backend
poetry install
poetry run uvicorn app.main:app --reload
\`\`\`

Key directories:
- /app/api - API routes
- /app/models - Database models
- /app/schemas - Pydantic schemas
- /app/services - Business logic
- /app/core - Core functionality

## Testing

### Running Tests
\`\`\`bash
# Backend tests
cd backend
poetry run pytest

# Frontend tests
cd frontend
npm run test
\`\`\`

## Deployment

### Production Setup
1. Configure domain and SSL
2. Set production environment variables
3. Build and deploy containers
4. Initialize database
5. Create super admin

### Minimum Requirements
- 2 CPU cores
- 4GB RAM
- 50GB SSD

## Security Features
- JWT-based authentication
- Role-based access control
- Data isolation per tenant
- Input validation
- CSRF protection
- Rate limiting

## Support
For support queries, contact:
- Technical support: support@schoolsaas.com
- Documentation: docs.schoolsaas.com

## License
MIT License - see LICENSE file for details