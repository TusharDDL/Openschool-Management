# School Management System - API Documentation

## API Overview

Base URL: `https://api.schoolmanagement.com/api/v1`

### Authentication
All API endpoints except authentication endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer <token>
```

## Table of Contents
1. [Authentication API](#authentication-api)
2. [School Management API](#school-management-api)
3. [Academic API](#academic-api)
4. [Student API](#student-api)
5. [Teacher API](#teacher-api)
6. [Finance API](#finance-api)
7. [Communication API](#communication-api)

## Authentication API

### Login
```http
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

Response:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "role": "school_admin",
    "name": "John Doe"
  }
}
```

### Refresh Token
```http
POST /auth/refresh
Content-Type: application/json

{
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

Response:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

## School Management API

### Create School
```http
POST /schools
Content-Type: application/json
Authorization: Bearer <token>

{
  "name": "Example School",
  "domain": "example",
  "admin_email": "admin@example.com",
  "contact_number": "+1234567890",
  "address": {
    "street": "123 Main St",
    "city": "Example City",
    "state": "Example State",
    "country": "Example Country",
    "postal_code": "12345"
  }
}
```

Response:
```json
{
  "id": 1,
  "name": "Example School",
  "domain": "example",
  "status": "active",
  "created_at": "2024-01-20T12:00:00Z",
  "admin": {
    "id": 2,
    "email": "admin@example.com",
    "role": "school_admin"
  }
}
```

### Get School Details
```http
GET /schools/{school_id}
Authorization: Bearer <token>
```

Response:
```json
{
  "id": 1,
  "name": "Example School",
  "domain": "example",
  "status": "active",
  "stats": {
    "total_students": 500,
    "total_teachers": 50,
    "total_classes": 20
  },
  "subscription": {
    "plan": "premium",
    "valid_until": "2025-01-20T12:00:00Z"
  }
}
```

## Academic API

### Create Class
```http
POST /academic/classes
Content-Type: application/json
Authorization: Bearer <token>

{
  "name": "Class 10A",
  "academic_year_id": 1,
  "section": "A",
  "capacity": 40,
  "class_teacher_id": 5
}
```

Response:
```json
{
  "id": 1,
  "name": "Class 10A",
  "section": "A",
  "capacity": 40,
  "class_teacher": {
    "id": 5,
    "name": "Jane Smith"
  },
  "created_at": "2024-01-20T12:00:00Z"
}
```

### Get Class Timetable
```http
GET /academic/classes/{class_id}/timetable
Authorization: Bearer <token>
```

Response:
```json
{
  "class_id": 1,
  "class_name": "Class 10A",
  "timetable": {
    "monday": [
      {
        "period": 1,
        "subject": "Mathematics",
        "teacher": "Mr. Johnson",
        "time": "08:00-09:00"
      }
    ]
  }
}
```

## Student API

### Create Student
```http
POST /students
Content-Type: application/json
Authorization: Bearer <token>

{
  "first_name": "John",
  "last_name": "Doe",
  "date_of_birth": "2010-01-01",
  "gender": "male",
  "admission_number": "2024001",
  "class_id": 1,
  "parent_details": {
    "father_name": "James Doe",
    "mother_name": "Jane Doe",
    "contact_number": "+1234567890",
    "email": "parent@example.com"
  }
}
```

Response:
```json
{
  "id": 1,
  "admission_number": "2024001",
  "full_name": "John Doe",
  "class": {
    "id": 1,
    "name": "Class 10A"
  },
  "status": "active",
  "created_at": "2024-01-20T12:00:00Z"
}
```

### Get Student Details
```http
GET /students/{student_id}
Authorization: Bearer <token>
```

Response:
```json
{
  "id": 1,
  "admission_number": "2024001",
  "personal_info": {
    "full_name": "John Doe",
    "date_of_birth": "2010-01-01",
    "gender": "male"
  },
  "academic_info": {
    "class": "Class 10A",
    "section": "A",
    "roll_number": "10"
  },
  "attendance": {
    "percentage": 95.5,
    "total_present": 85,
    "total_absent": 4
  }
}
```

## Finance API

### Create Fee Structure
```http
POST /finance/fee-structures
Content-Type: application/json
Authorization: Bearer <token>

{
  "name": "Tuition Fee",
  "amount": 5000,
  "frequency": "MONTHLY",
  "academic_year_id": 1,
  "class_id": 1,
  "due_day": 5
}
```

Response:
```json
{
  "id": 1,
  "name": "Tuition Fee",
  "amount": 5000,
  "frequency": "MONTHLY",
  "academic_year": "2024-25",
  "class": "Class 10A",
  "created_at": "2024-01-20T12:00:00Z"
}
```

### Record Payment
```http
POST /finance/payments
Content-Type: application/json
Authorization: Bearer <token>

{
  "student_id": 1,
  "fee_structure_id": 1,
  "amount": 5000,
  "payment_mode": "ONLINE",
  "transaction_id": "txn_123456",
  "payment_date": "2024-01-20"
}
```

Response:
```json
{
  "id": 1,
  "receipt_number": "REC2024001",
  "amount": 5000,
  "status": "success",
  "transaction_details": {
    "mode": "ONLINE",
    "transaction_id": "txn_123456"
  },
  "created_at": "2024-01-20T12:00:00Z"
}
```

## Communication API

### Create Announcement
```http
POST /communication/announcements
Content-Type: application/json
Authorization: Bearer <token>

{
  "title": "Parent Teacher Meeting",
  "content": "PTM scheduled for Class 10 on 25th January",
  "target_audience": {
    "classes": [1, 2],
    "roles": ["student", "parent"]
  },
  "schedule_at": "2024-01-23T10:00:00Z"
}
```

Response:
```json
{
  "id": 1,
  "title": "Parent Teacher Meeting",
  "status": "scheduled",
  "target_reach": 150,
  "scheduled_at": "2024-01-23T10:00:00Z",
  "created_at": "2024-01-20T12:00:00Z"
}
```

### Get Notifications
```http
GET /communication/notifications
Authorization: Bearer <token>
```

Response:
```json
{
  "notifications": [
    {
      "id": 1,
      "type": "ANNOUNCEMENT",
      "title": "Parent Teacher Meeting",
      "content": "PTM scheduled for Class 10",
      "read": false,
      "created_at": "2024-01-20T12:00:00Z"
    }
  ],
  "unread_count": 1
}
```

## Error Responses

### 400 Bad Request
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": {
      "field": ["error message"]
    }
  }
}
```

### 401 Unauthorized
```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Invalid or expired token"
  }
}
```

### 403 Forbidden
```json
{
  "error": {
    "code": "FORBIDDEN",
    "message": "Insufficient permissions"
  }
}
```

### 404 Not Found
```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "Resource not found"
  }
}
```

## Rate Limiting

API requests are limited to:
- 100 requests per minute for authenticated users
- 20 requests per minute for unauthenticated users

Rate limit headers:
```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1579521600
```

## Pagination

List endpoints support pagination using query parameters:
```http
GET /students?page=1&limit=10
```

Response includes pagination metadata:
```json
{
  "data": [...],
  "pagination": {
    "total": 100,
    "page": 1,
    "limit": 10,
    "pages": 10
  }
}
```

## Filtering and Sorting

### Filtering
Use query parameters for filtering:
```http
GET /students?class_id=1&status=active
```

### Sorting
Use `sort` parameter for sorting:
```http
GET /students?sort=name:asc,created_at:desc
```

## WebSocket API

### Connection
```javascript
const ws = new WebSocket('wss://api.schoolmanagement.com/ws');
ws.onopen = () => {
  ws.send(JSON.stringify({
    type: 'auth',
    token: 'Bearer token'
  }));
};
```

### Event Types

#### Notifications
```json
{
  "type": "notification",
  "data": {
    "id": 1,
    "title": "New Announcement",
    "content": "School closed tomorrow"
  }
}
```

#### Real-time Updates
```json
{
  "type": "update",
  "resource": "attendance",
  "data": {
    "student_id": 1,
    "status": "present",
    "timestamp": "2024-01-20T12:00:00Z"
  }
}
```