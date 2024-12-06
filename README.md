# School Management SaaS Platform

A comprehensive multi-tenant SaaS solution for efficient school management, offering features from academic management to financial operations.

## Features

### 1. Multi-tenant Architecture
- Isolated data per school
- Customizable configurations
- Role-based access control
- School-specific branding options

### 2. Financial Management
- **Fee Structure**
  - Class/section/student-specific plans
  - Flexible payment schedules (monthly, quarterly, yearly)
  - Custom due dates
  - Discount management with approval workflow
- **Payment Processing**
  - Transaction tracking with unique IDs
  - Payment history
  - Exportable reports
  - Receipt generation

### 3. Academic Management
- **Timetable Management**
  - Class/section-wise scheduling
  - Weekly templates
  - Teacher allocation
  - Conflict detection
- **Assessment System**
  - Multiple assessment types
  - Custom grading patterns
  - Result generation
  - Performance analytics
- **Resource Management**
  - Study material uploads
  - Assignment management
  - Digital library

### 4. Student Management
- **Profile Management**
  - Academic records
  - Attendance tracking
  - Performance monitoring
  - Emergency contacts
- **Portal Access**
  - Fee payment history
  - Academic performance
  - Assignment submissions
  - Attendance records

### 5. Communication
- **Announcements**
  - Role-based targeting
  - Class/section-specific notices
  - School-wide broadcasts
- **Notifications**
  - Fee reminders
  - Assignment deadlines
  - Exam schedules
  - Event updates

## Getting Started

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for frontend development)
- Python 3.11+ (for backend development)
- PostgreSQL 15+
- Redis 7+

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/school-management.git
cd school-management
```

2. Backend Setup:
```bash
# Create and activate virtual environment
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOL
DATABASE_URL=postgresql://postgres:Tushar@098@34.131.42.0:5432/postgres
ASYNC_DATABASE_URL=postgresql+asyncpg://postgres:Tushar@098@34.131.42.0:5432/postgres

# Redis settings
REDIS_URL=redis://localhost:6379/0

# Security settings
SECRET_KEY=your-secret-key-here-min-32-chars-long123
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Email settings (optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
EOL

# Install and start Redis
sudo apt update
sudo apt install -y redis-server
sudo systemctl start redis-server

# Run migrations
PYTHONPATH=/path/to/School-Management/backend alembic upgrade head

# Start backend server
PYTHONPATH=/path/to/School-Management/backend uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

3. Frontend Setup:
```bash
# Install dependencies
cd ..  # Back to project root
npm install --legacy-peer-deps

# Create .env.local file
cat > .env.local << EOL
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_WEBSOCKET_URL=ws://localhost:8000/ws
NEXT_PUBLIC_UPLOAD_URL=http://localhost:8000/uploads
NEXT_PUBLIC_MAX_FILE_SIZE=5242880
EOL

# Start frontend development server
npm run dev
```

4. Create initial superuser:
```bash
cd backend
PYTHONPATH=/path/to/School-Management/backend python scripts/create_superuser.py
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Development Setup

1. Frontend Development:
```bash
cd frontend
npm install
npm run dev
```

2. Backend Development:
```bash
cd backend
poetry install
poetry run uvicorn app.main:app --reload
```

## Admin Operations Guide

### School Onboarding
1. Create tenant for the school
2. Configure school details and branding
3. Set up academic structure (classes, sections)
4. Create initial admin accounts
5. Configure fee structure

### Role Management
- **Super Admin**: Platform-level administration
- **School Admin**: School-specific management
- **Teacher**: Academic operations
- **Student/Parent**: Limited access to relevant features

### Financial Operations
1. Setting up fee structures
2. Managing payment schedules
3. Processing fee payments
4. Handling discounts
5. Generating financial reports

## API Documentation

### Authentication
```bash
POST /api/v1/auth/login
POST /api/v1/auth/register
POST /api/v1/auth/logout
```

### Student Management
```bash
GET /api/v1/students
POST /api/v1/students
GET /api/v1/students/{id}
PUT /api/v1/students/{id}
```

### Financial Management
```bash
POST /api/v1/fees
GET /api/v1/fees
POST /api/v1/fees/pay
GET /api/v1/fees/report
```

### Academic Management
```bash
POST /api/v1/academic/timetable
GET /api/v1/academic/timetable
POST /api/v1/academic/assignments
GET /api/v1/academic/results
```

## Deployment Guide

### Production Setup
1. Configure production environment variables
2. Set up SSL certificates
3. Configure backup strategy
4. Set up monitoring

### Infrastructure Requirements
- **Minimum**:
  - 2 CPU cores
  - 4GB RAM
  - 50GB SSD
- **Recommended**:
  - 4 CPU cores
  - 8GB RAM
  - 100GB SSD

### Scaling Considerations
- Database replication
- Load balancing
- Caching strategy
- File storage optimization

## Security Measures

1. **Authentication & Authorization**
   - JWT-based authentication
   - Role-based access control
   - Token expiration and refresh
   - Session management

2. **Data Protection**
   - Data encryption at rest
   - Secure communication (HTTPS)
   - Input validation
   - CSRF protection

3. **API Security**
   - Rate limiting
   - Request validation
   - Error handling
   - Audit logging

## Testing

### Running Tests
```bash
# Backend tests
cd backend
poetry run pytest

# Frontend tests
cd frontend
npm run test
```

### Test Coverage
- Unit tests
- Integration tests
- End-to-end tests
- Performance tests

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support


