# OpenHands School Management System API Documentation

## Base URL
```
http://localhost:8000/api/v1
```

## Authentication

### Login
```http
POST /auth/login
```

**Request Body:**
```json
{
    "email": "admin@example.com",
    "password": "Admin123"
}
```

**Response:**
```json
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "token_type": "bearer"
}
```

## Academic Management

### Academic Years

#### Create Academic Year
```http
POST /academic/years
```

**Request Body:**
```json
{
    "name": "2024-25",
    "start_date": "2024-04-01",
    "end_date": "2025-03-31",
    "is_active": true,
    "tenant_id": 1,
    "school_id": 1
}
```

#### List Academic Years
```http
GET /academic/years
```

#### Get Academic Year
```http
GET /academic/years/{id}
```

#### Update Academic Year
```http
PUT /academic/years/{id}
```

### Classes

#### Create Class
```http
POST /academic/classes
```

**Request Body:**
```json
{
    "name": "Class 10",
    "grade_level": 10,
    "academic_year_id": 1,
    "is_active": true,
    "tenant_id": 1,
    "school_id": 1
}
```

#### List Classes
```http
GET /academic/classes
```

#### Get Class
```http
GET /academic/classes/{id}
```

#### Update Class
```http
PUT /academic/classes/{id}
```

### Sections

#### Create Section
```http
POST /academic/sections
```

**Request Body:**
```json
{
    "name": "Section A",
    "class_id": 1,
    "capacity": 40,
    "is_active": true,
    "tenant_id": 1
}
```

#### List Sections
```http
GET /academic/sections
```

#### Get Section
```http
GET /academic/sections/{id}
```

#### Update Section
```http
PUT /academic/sections/{id}
```

### Subjects

#### Create Subject
```http
POST /subjects
```

**Request Body:**
```json
{
    "name": "Mathematics",
    "code": "MATH10",
    "description": "Mathematics for Class 10",
    "credits": 5.0,
    "is_active": true,
    "tenant_id": 1,
    "school_id": 1
}
```

#### List Subjects
```http
GET /subjects
```

#### Get Subject
```http
GET /subjects/{id}
```

#### Update Subject
```http
PUT /subjects/{id}
```

## Student Management

### Create Student
```http
POST /students
```

**Request Body:**
```json
{
    "first_name": "John",
    "last_name": "Doe",
    "date_of_birth": "2010-01-01",
    "gender": "male",
    "email": "john.doe@example.com",
    "phone": "1234567890",
    "address": "123 Main St",
    "tenant_id": 1,
    "school_id": 1
}
```

### List Students
```http
GET /students
```

### Get Student
```http
GET /students/{id}
```

### Update Student
```http
PUT /students/{id}
```

### Delete Student
```http
DELETE /students/{id}
```

## Teacher Management

### Create Teacher
```http
POST /teachers
```

**Request Body:**
```json
{
    "first_name": "Jane",
    "last_name": "Smith",
    "date_of_birth": "1990-01-01",
    "gender": "female",
    "email": "jane.smith@example.com",
    "phone": "1234567890",
    "address": "456 Oak St",
    "tenant_id": 1,
    "school_id": 1,
    "subjects": [1, 2]
}
```

### List Teachers
```http
GET /teachers
```

### Get Teacher
```http
GET /teachers/{id}
```

### Update Teacher
```http
PUT /teachers/{id}
```

### Delete Teacher
```http
DELETE /teachers/{id}
```

## Attendance Management

### Create Attendance
```http
POST /attendance
```

**Request Body:**
```json
{
    "student_id": 1,
    "section_id": 1,
    "date": "2024-01-01",
    "status": "present",
    "remarks": "On time"
}
```

### List Attendance
```http
GET /attendance
```

### Get Attendance
```http
GET /attendance/{id}
```

### Update Attendance
```http
PUT /attendance/{id}
```

## Fee Management

### Create Fee
```http
POST /fees
```

**Request Body:**
```json
{
    "student_id": 1,
    "fee_type": "tuition",
    "amount": 1000.00,
    "due_date": "2024-01-01",
    "status": "pending"
}
```

### List Fees
```http
GET /fees
```

### Get Fee
```http
GET /fees/{id}
```

### Update Fee
```http
PUT /fees/{id}
```

## Assessment Management

### Create Assessment
```http
POST /assessments
```

**Request Body:**
```json
{
    "name": "Mid Term",
    "subject_id": 1,
    "section_id": 1,
    "date": "2024-01-01",
    "total_marks": 100,
    "passing_marks": 40
}
```

### List Assessments
```http
GET /assessments
```

### Get Assessment
```http
GET /assessments/{id}
```

### Update Assessment
```http
PUT /assessments/{id}
```

## Results Management

### Create Result
```http
POST /results
```

**Request Body:**
```json
{
    "student_id": 1,
    "assessment_id": 1,
    "marks_obtained": 85,
    "remarks": "Excellent"
}
```

### List Results
```http
GET /results
```

### Get Result
```http
GET /results/{id}
```

### Update Result
```http
PUT /results/{id}
```

## Timetable Management

### Create Timetable
```http
POST /academic/timetable
```

**Request Body:**
```json
{
    "section_id": 1,
    "subject_id": 1,
    "teacher_id": 1,
    "day": "monday",
    "start_time": "09:00:00",
    "end_time": "10:00:00"
}
```

### List Timetable
```http
GET /academic/timetable
```

### Get Timetable Entry
```http
GET /academic/timetable/{id}
```

### Update Timetable Entry
```http
PUT /academic/timetable/{id}
```

## Communication

### Create Announcement
```http
POST /announcements
```

**Request Body:**
```json
{
    "title": "School Closed",
    "content": "School will be closed tomorrow due to heavy rain",
    "type": "general",
    "target_audience": ["students", "teachers"]
}
```

### List Announcements
```http
GET /announcements
```

### Get Announcement
```http
GET /announcements/{id}
```

### Update Announcement
```http
PUT /announcements/{id}
```

## Resource Management

### Create Resource
```http
POST /resources
```

**Request Body:**
```json
{
    "title": "Math Notes",
    "description": "Class 10 Math Notes",
    "type": "notes",
    "url": "https://example.com/notes.pdf",
    "subject_id": 1
}
```

### List Resources
```http
GET /resources
```

### Get Resource
```http
GET /resources/{id}
```

### Update Resource
```http
PUT /resources/{id}
```

### Delete Resource
```http
DELETE /resources/{id}
```

## Error Responses

### 400 Bad Request
```json
{
    "detail": "Invalid request parameters"
}
```

### 401 Unauthorized
```json
{
    "detail": "Could not validate credentials"
}
```

### 403 Forbidden
```json
{
    "detail": "Not enough permissions"
}
```

### 404 Not Found
```json
{
    "detail": "Resource not found"
}
```

### 422 Validation Error
```json
{
    "detail": [
        {
            "loc": ["body", "field_name"],
            "msg": "field required",
            "type": "value_error.missing"
        }
    ]
}
```

### 429 Too Many Requests
```json
{
    "detail": "Too many requests"
}
```

### 500 Internal Server Error
```json
{
    "detail": "Internal server error"
}
```