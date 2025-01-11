# School Management System API Documentation

## Base URL
```
http://localhost:8000/api/v1
```

## Authentication
Most endpoints require authentication using JWT tokens. Include the token in the Authorization header:
```
Authorization: Bearer YOUR_ACCESS_TOKEN
```

## API Endpoints

### Authentication

#### 1. Login
- **Endpoint**: `/auth/login`
- **Method**: POST
- **Description**: Authenticate user and get access token
- **Request Body**:
```json
{
    "email": "user@example.com",
    "password": "password123"
}
```
- **Response**:
```json
{
    "access_token": "eyJhbGc...",
    "token_type": "bearer"
}
```

# API Groups

## 1. Authentication API (/auth)

### 1.1. Login
- **Endpoint**: `/auth/login`
- **Method**: POST
- **Description**: Authenticate user and get access token
- **Request Body**:
```json
{
    "email": "user@example.com",
    "password": "password123"
}
```
- **Response**:
```json
{
    "access_token": "eyJhbGc...",
    "token_type": "bearer"
}
```

### 1.2. Register User
- **Endpoint**: `/auth/register`
- **Method**: POST
- **Description**: Register a new user (requires admin privileges)
- **Authentication**: Required
- **Request Body**:
```json
{
    "username": "newuser",
    "email": "newuser@example.com",
    "password": "password123",
    "role": "SCHOOL_ADMIN",
    "tenant_id": 1,
    "is_active": true
}
```
- **Response**:
```json
{
    "message": "User created successfully",
    "user_id": 1
}
```

### 1.3. Get Current User Info
- **Endpoint**: `/auth/me`
- **Method**: GET
- **Description**: Get current user information
- **Authentication**: Required
- **Response**:
```json
{
    "id": 1,
    "email": "user@example.com",
    "username": "username",
    "role": "SCHOOL_ADMIN",
    "is_active": true,
    "tenant_id": 1,
    "is_saas_admin": false
}
```

### 1.4. Logout
- **Endpoint**: `/auth/logout`
- **Method**: POST
- **Description**: Logout user (client should discard token)
- **Authentication**: Required
- **Response**:
```json
{
    "message": "Successfully logged out"
}
```

## 2. Tenants API (/tenants)

### 2.1. Create Tenant
- **Endpoint**: `/tenants`
- **Method**: POST
- **Description**: Create a new tenant (Super Admin only)
- **Authentication**: Required (Super Admin)
- **Request Body**:
```json
{
    "name": "Demo School",
    "subdomain": "demo",
    "address": "123 Demo St",
    "contact_email": "demo@example.com",
    "contact_phone": "1234567890"
}
```
- **Response**:
```json
{
    "id": 1,
    "name": "Demo School",
    "subdomain": "demo",
    "address": "123 Demo St",
    "contact_email": "demo@example.com",
    "contact_phone": "1234567890",
    "created_at": "2024-03-20T10:00:00",
    "updated_at": "2024-03-20T10:00:00"
}
```

### 2.2. List Tenants
- **Endpoint**: `/tenants`
- **Method**: GET
- **Description**: List all tenants (Super Admin only)
- **Authentication**: Required (Super Admin)
- **Query Parameters**:
  - skip: int (optional, default: 0)
  - limit: int (optional, default: 100)
- **Response**:
```json
[
    {
        "id": 1,
        "name": "Demo School",
        "subdomain": "demo",
        "address": "123 Demo St",
        "contact_email": "demo@example.com",
        "contact_phone": "1234567890",
        "created_at": "2024-03-20T10:00:00",
        "updated_at": "2024-03-20T10:00:00"
    }
]
```

### 2.3. Get Tenant
- **Endpoint**: `/tenants/{tenant_id}`
- **Method**: GET
- **Description**: Get tenant by ID (Super Admin only)
- **Authentication**: Required (Super Admin)
- **Response**:
```json
{
    "id": 1,
    "name": "Demo School",
    "subdomain": "demo",
    "address": "123 Demo St",
    "contact_email": "demo@example.com",
    "contact_phone": "1234567890",
    "created_at": "2024-03-20T10:00:00",
    "updated_at": "2024-03-20T10:00:00"
}
```

### 2.4. Update Tenant
- **Endpoint**: `/tenants/{tenant_id}`
- **Method**: PUT
- **Description**: Update tenant details (Super Admin only)
- **Authentication**: Required (Super Admin)
- **Request Body**:
```json
{
    "name": "Updated School Name",
    "address": "456 New Address",
    "contact_email": "new@example.com",
    "contact_phone": "9876543210"
}
```
- **Response**: Updated tenant object

### 2.5. Delete Tenant
- **Endpoint**: `/tenants/{tenant_id}`
- **Method**: DELETE
- **Description**: Delete tenant (Super Admin only)
- **Authentication**: Required (Super Admin)
- **Response**: No content (204)

## 3. Schools API (/schools)

### 3.1. Create School
- **Endpoint**: `/schools`
- **Method**: POST
- **Description**: Create a new school (School Admin or higher)
- **Authentication**: Required
- **Request Body**:
```json
{
    "name": "Demo High School",
    "tenant_id": 1,
    "address": "456 School St",
    "contact_email": "school@example.com",
    "contact_phone": "1234567890",
    "principal_name": "John Doe",
    "website": "https://demo-school.com"
}
```
- **Response**:
```json
{
    "id": 1,
    "name": "Demo High School",
    "tenant_id": 1,
    "address": "456 School St",
    "phone": null,
    "created_at": "2024-03-20T10:00:00+00:00",
    "updated_at": "2024-03-20T10:00:00+00:00"
}
```

### 3.2. List Schools
- **Endpoint**: `/schools`
- **Method**: GET
- **Description**: List schools (filtered by tenant_id if provided)
- **Authentication**: Required
- **Query Parameters**:
  - tenant_id: int (optional) - Filter schools by tenant ID
  - skip: int (optional, default: 0)
  - limit: int (optional, default: 100)
- **Response**:
```json
[
    {
        "id": 1,
        "name": "Demo High School",
        "tenant_id": 1,
        "address": "456 School St",
        "phone": null,
        "created_at": "2024-03-20T10:00:00+00:00",
        "updated_at": "2024-03-20T10:00:00+00:00"
    }
]
```

### 3.3. Get School
- **Endpoint**: `/schools/{school_id}`
- **Method**: GET
- **Description**: Get school by ID
- **Authentication**: Required
- **Response**:
```json
{
    "id": 1,
    "name": "Demo High School",
    "tenant_id": 1,
    "address": "456 School St",
    "phone": null,
    "created_at": "2024-03-20T10:00:00+00:00",
    "updated_at": "2024-03-20T10:00:00+00:00"
}
```

### 3.4. Update School
- **Endpoint**: `/schools/{school_id}`
- **Method**: PUT
- **Description**: Update school details (School Admin or higher)
- **Authentication**: Required
- **Request Body**:
```json
{
    "name": "Updated School Name",
    "address": "456 New Address",
    "contact_email": "new@example.com",
    "contact_phone": "9876543210",
    "principal_name": "Jane Doe",
    "website": "https://updated-school.com"
}
```
- **Response**: Updated school object

### 3.5. Delete School
- **Endpoint**: `/schools/{school_id}`
- **Method**: DELETE
- **Description**: Delete school (School Admin or higher)
- **Authentication**: Required
- **Response**: No content (204)

## 4. Students API (/students)

### 4.1. Create Student
- **Endpoint**: `/students`
- **Method**: POST
- **Description**: Create a new student profile (School Admin only)
- **Authentication**: Required
- **Request Body**:
```json
{
    "first_name": "John",
    "last_name": "Doe",
    "date_of_birth": "2010-01-01",
    "gender": "MALE",
    "admission_number": "2024001",
    "admission_date": "2024-01-01",
    "school_id": 1,
    "class_id": 1,
    "section_id": 1,
    "blood_group": "O+",
    "address": "123 Student St",
    "contact_phone": "1234567890",
    "emergency_contact": "9876543210",
    "is_active": true
}
```
- **Response**: Created student profile

### 4.2. List Students
- **Endpoint**: `/students`
- **Method**: GET
- **Description**: List students with optional filtering
- **Authentication**: Required
- **Query Parameters**:
  - search: string (optional) - Search by name or admission number
  - class_id: int (optional) - Filter by class
  - section_id: int (optional) - Filter by section
  - is_active: boolean (optional) - Filter by active status
  - skip: int (optional, default: 0)
  - limit: int (optional, default: 100, max: 100)
- **Response**:
```json
[
    {
        "id": 1,
        "first_name": "John",
        "last_name": "Doe",
        "admission_number": "2024001",
        "class_name": "Class 1",
        "section_name": "Section A",
        "is_active": true
    }
]
```

### 4.3. Get Student Details
- **Endpoint**: `/students/{student_id}`
- **Method**: GET
- **Description**: Get detailed student information
- **Authentication**: Required
- **Response**:
```json
{
    "id": 1,
    "first_name": "John",
    "last_name": "Doe",
    "date_of_birth": "2010-01-01",
    "gender": "MALE",
    "admission_number": "2024001",
    "admission_date": "2024-01-01",
    "school_id": 1,
    "blood_group": "O+",
    "address": "123 Student St",
    "contact_phone": "1234567890",
    "emergency_contact": "9876543210",
    "is_active": true,
    "current_section": "Section A",
    "current_class": "Class 1",
    "academic_year": "2024-25",
    "attendance_summary": {
        "total_days": 100,
        "present_days": 95,
        "absent_days": 5,
        "attendance_percentage": 95.0
    }
}
```

### 4.4. Update Student
- **Endpoint**: `/students/{student_id}`
- **Method**: PUT
- **Description**: Update student profile (School Admin only)
- **Authentication**: Required
- **Request Body**: Same as create student (all fields optional)
- **Response**: Updated student profile

### 4.5. Add Guardian
- **Endpoint**: `/students/{student_id}/guardians`
- **Method**: POST
- **Description**: Add a guardian to a student (School Admin only)
- **Authentication**: Required
- **Request Body**:
```json
{
    "name": "Jane Doe",
    "relationship": "MOTHER",
    "occupation": "Engineer",
    "contact_phone": "1234567890",
    "email": "jane@example.com",
    "address": "123 Guardian St",
    "is_primary": true
}
```
- **Response**: Created guardian profile

### 4.6. Update Guardian
- **Endpoint**: `/students/guardians/{guardian_id}`
- **Method**: PUT
- **Description**: Update guardian information (School Admin only)
- **Authentication**: Required
- **Request Body**: Same as add guardian (all fields optional)
- **Response**: Updated guardian profile

### 4.7. Upload Document
- **Endpoint**: `/students/{student_id}/documents`
- **Method**: POST
- **Description**: Upload a document for a student (School Admin only)
- **Authentication**: Required
- **Request Body**: Multipart form data
  - document_type: string
  - file: file upload
- **Response**: Created document record

### 4.8. Verify Document
- **Endpoint**: `/students/documents/{document_id}/verify`
- **Method**: POST
- **Description**: Verify a student document (School Admin only)
- **Authentication**: Required
- **Response**: Updated document record

### 4.9. Add Note
- **Endpoint**: `/students/{student_id}/notes`
- **Method**: POST
- **Description**: Add a note to a student (Teacher or higher)
- **Authentication**: Required
- **Request Body**:
```json
{
    "note_type": "ACADEMIC",
    "content": "Student shows great progress in mathematics",
    "visibility": "STAFF_ONLY"
}
```
- **Response**: Created note

### 4.10. Get Student Notes
- **Endpoint**: `/students/{student_id}/notes`
- **Method**: GET
- **Description**: Get student notes (Teacher or higher)
- **Authentication**: Required
- **Query Parameters**:
  - note_type: string (optional) - Filter by note type
- **Response**: List of notes

### 4.11. Get Attendance Summary
- **Endpoint**: `/students/{student_id}/attendance`
- **Method**: GET
- **Description**: Get student attendance summary
- **Authentication**: Required
- **Query Parameters**:
  - start_date: date (optional) - Filter by start date
  - end_date: date (optional) - Filter by end date
- **Response**:
```json
{
    "total_days": 100,
    "present_days": 95,
    "absent_days": 5,
    "attendance_percentage": 95.0,
    "attendance_by_month": [
        {
            "month": "2024-01",
            "total_days": 22,
            "present_days": 21,
            "absent_days": 1
        }
    ]
}
```

## 5. Academic API (/academic)

### 5.1. Academic Years

#### 5.1.1. Create Academic Year
- **Endpoint**: `/academic/years`
- **Method**: POST
- **Description**: Create a new academic year (School Admin only)
- **Authentication**: Required
- **Request Body**:
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
- **Response**: Created academic year

#### 5.1.2. List Academic Years
- **Endpoint**: `/academic/years`
- **Method**: GET
- **Description**: List academic years
- **Authentication**: Required
- **Query Parameters**:
  - is_active: boolean (optional) - Filter by active status
  - skip: int (optional, default: 0)
  - limit: int (optional, default: 100)
- **Response**: List of academic years

#### 5.1.3. Get Academic Year
- **Endpoint**: `/academic/years/{year_id}`
- **Method**: GET
- **Description**: Get academic year by ID
- **Authentication**: Required
- **Response**: Academic year details

#### 5.1.4. Update Academic Year
- **Endpoint**: `/academic/years/{year_id}`
- **Method**: PUT
- **Description**: Update academic year (School Admin only)
- **Authentication**: Required
- **Request Body**: Same as create (all fields optional)
- **Response**: Updated academic year

### 5.2. Classes

#### 5.2.1. Create Class
- **Endpoint**: `/academic/classes`
- **Method**: POST
- **Description**: Create a new class (School Admin only)
- **Authentication**: Required
- **Request Body**:
```json
{
    "name": "Class 1",
    "academic_year_id": 1,
    "school_id": 1,
    "tenant_id": 1,
    "grade_level": 1,
    "is_active": true
}
```
- **Response**: Created class

#### 5.2.2. List Classes
- **Endpoint**: `/academic/classes`
- **Method**: GET
- **Description**: List classes
- **Authentication**: Required
- **Query Parameters**:
  - academic_year_id: int (optional) - Filter by academic year
  - is_active: boolean (optional) - Filter by active status
  - skip: int (optional, default: 0)
  - limit: int (optional, default: 100)
- **Response**: List of classes

#### 5.2.3. Get Class
- **Endpoint**: `/academic/classes/{class_id}`
- **Method**: GET
- **Description**: Get class by ID
- **Authentication**: Required
- **Response**: Class details

#### 5.2.4. Update Class
- **Endpoint**: `/academic/classes/{class_id}`
- **Method**: PUT
- **Description**: Update class (School Admin only)
- **Authentication**: Required
- **Request Body**: Same as create (all fields optional)
- **Response**: Updated class

### 5.3. Sections

#### 5.3.1. Create Section
- **Endpoint**: `/academic/sections`
- **Method**: POST
- **Description**: Create a new section (School Admin only)
- **Authentication**: Required
- **Request Body**:
```json
{
    "name": "Section A",
    "class_id": 1,
    "tenant_id": 1,
    "school_id": 1,
    "capacity": 30,
    "is_active": true
}
```
- **Response**: Created section

#### 5.3.2. List Sections
- **Endpoint**: `/academic/sections`
- **Method**: GET
- **Description**: List sections
- **Authentication**: Required
- **Query Parameters**:
  - class_id: int (optional) - Filter by class
  - is_active: boolean (optional) - Filter by active status
  - skip: int (optional, default: 0)
  - limit: int (optional, default: 100)
- **Response**: List of sections

#### 5.3.3. Get Section
- **Endpoint**: `/academic/sections/{section_id}`
- **Method**: GET
- **Description**: Get section by ID
- **Authentication**: Required
- **Response**: Section details

#### 5.3.4. Update Section
- **Endpoint**: `/academic/sections/{section_id}`
- **Method**: PUT
- **Description**: Update section (School Admin only)
- **Authentication**: Required
- **Request Body**: Same as create (all fields optional)
- **Response**: Updated section

### 5.4. Student-Section Assignment

#### 5.4.1. Assign Student to Section
- **Endpoint**: `/academic/student-sections`
- **Method**: POST
- **Description**: Assign a student to a section (School Admin only)
- **Authentication**: Required
- **Request Body**:
```json
{
    "student_id": 1,
    "section_id": 1,
    "academic_year_id": 1,
    "tenant_id": 1,
    "is_active": true
}
```
- **Response**: Created assignment

### 5.5. Teacher-Section Assignment

#### 5.5.1. Assign Teacher to Section
- **Endpoint**: `/academic/teacher-sections`
- **Method**: POST
- **Description**: Assign a teacher to a section (School Admin only)
- **Authentication**: Required
- **Request Body**:
```json
{
    "teacher_id": 1,
    "section_id": 1,
    "subject_id": 1,
    "academic_year_id": 1,
    "tenant_id": 1,
    "is_active": true
}
```
- **Response**: Created assignment

### 5.6. Utility Endpoints

#### 5.6.1. Get Class Students
- **Endpoint**: `/academic/classes/{class_id}/students`
- **Method**: GET
- **Description**: Get all students in a class (Teacher or higher)
- **Authentication**: Required
- **Query Parameters**:
  - is_active: boolean (optional) - Filter by active status
- **Response**: List of students in the class

#### 5.6.2. Get Teacher Classes
- **Endpoint**: `/academic/teachers/{teacher_id}/classes`
- **Method**: GET
- **Description**: Get all classes assigned to a teacher
- **Authentication**: Required
- **Query Parameters**:
  - academic_year_id: int (optional) - Filter by academic year
- **Response**: List of classes assigned to the teacher

## 6. Attendance API (/attendance)

### 6.1. Mark Attendance
- **Endpoint**: `/attendance`
- **Method**: POST
- **Description**: Mark attendance for a student
- **Authentication**: Required
- **Request Body**:
```json
{
    "student_id": 1,
    "date": "2024-12-18",
    "status": "PRESENT",
    "remarks": "On time",
    "tenant_id": 1,
    "school_id": 1
}
```
- **Response**: Created attendance record

### 6.2. Get Student Attendance
- **Endpoint**: `/attendance/student/{student_id}`
- **Method**: GET
- **Description**: Get attendance records for a student
- **Authentication**: Required
- **Query Parameters**:
  - start_date: date (required) - Start date for attendance records
  - end_date: date (required) - End date for attendance records
- **Response**: List of attendance records

### 6.3. Get Class Attendance
- **Endpoint**: `/attendance/class/{class_id}`
- **Method**: GET
- **Description**: Get attendance records for a class on a specific date
- **Authentication**: Required
- **Query Parameters**:
  - date: date (required) - Date for attendance records
- **Response**: List of attendance records

### 6.4. Update Attendance
- **Endpoint**: `/attendance/{attendance_id}`
- **Method**: PUT
- **Description**: Update an attendance record
- **Authentication**: Required
- **Request Body**:
```json
{
    "status": "ABSENT",
    "remarks": "Parent informed"
}
```
- **Response**: Updated attendance record

### 6.5. Get Attendance Report
- **Endpoint**: `/attendance/report`
- **Method**: GET
- **Description**: Get attendance report for a class
- **Authentication**: Required
- **Query Parameters**:
  - class_id: int (required) - Class ID
  - start_date: date (required) - Start date for report
  - end_date: date (required) - End date for report
- **Response**:
```json
{
    "class_id": 1,
    "class_name": "Class 1",
    "start_date": "2024-12-01",
    "end_date": "2024-12-31",
    "total_students": 30,
    "total_days": 22,
    "attendance_summary": {
        "present": 600,
        "absent": 60,
        "late": 20,
        "average_attendance": 95.0
    },
    "daily_attendance": [
        {
            "date": "2024-12-18",
            "present": 28,
            "absent": 2,
            "late": 1,
            "attendance_percentage": 93.33
        }
    ],
    "student_wise_summary": [
        {
            "student_id": 1,
            "name": "John Doe",
            "present_days": 20,
            "absent_days": 2,
            "late_days": 0,
            "attendance_percentage": 90.91
        }
    ]
}
```

## 7. Fees API (/fees)

### 7.1. Create Fee Structure
- **Endpoint**: `/fees`
- **Method**: POST
- **Description**: Create a new fee structure (School Admin only)
- **Authentication**: Required
- **Request Body**:
```json
{
    "name": "Tuition Fee",
    "fee_type": "TUITION",
    "amount": 5000,
    "interval": "MONTHLY",
    "academic_year": "2024-25",
    "academic_year_id": 1,
    "class_id": 1,
    "school_id": 1,
    "tenant_id": 1,
    "is_active": true,
    "due_day": 5,
    "late_fee": 100
}
```
- **Response**: Created fee structure

### 7.2. List Fee Structures
- **Endpoint**: `/fees`
- **Method**: GET
- **Description**: List fee structures with optional filters
- **Authentication**: Required
- **Query Parameters**:
  - class_id: int (optional) - Filter by class ID
  - section_id: int (optional) - Filter by section ID
  - fee_type: string (optional) - Filter by fee type (TUITION, TRANSPORT, etc.)
- **Response**: List of fee structures

### 7.3. Create Fee Discount
- **Endpoint**: `/fees/discounts`
- **Method**: POST
- **Description**: Create a fee discount (School Admin only)
- **Authentication**: Required
- **Request Body**:
```json
{
    "student_id": 1,
    "fee_structure_id": 1,
    "discount_type": "PERCENTAGE",
    "discount_value": 10,
    "reason": "Sibling discount",
    "valid_from": "2024-04-01",
    "valid_until": "2025-03-31",
    "is_active": true
}
```
- **Response**: Created discount

### 7.4. Record Fee Payment
- **Endpoint**: `/fees/pay`
- **Method**: POST
- **Description**: Record a fee payment
- **Authentication**: Required
- **Request Body**:
```json
{
    "student_id": 1,
    "fee_structure_id": 1,
    "amount_paid": 5000,
    "payment_date": "2024-12-18",
    "payment_method": "ONLINE",
    "transaction_reference": "TXN123456",
    "remarks": "December tuition fee"
}
```
- **Response**: Created transaction record

### 7.5. Get Student Pending Fees
- **Endpoint**: `/fees/student/{student_id}/pending`
- **Method**: GET
- **Description**: Get pending fees for a student
- **Authentication**: Required
- **Response**: List of pending fee structures

### 7.6. Generate Fee Report
- **Endpoint**: `/fees/report`
- **Method**: POST
- **Description**: Generate fee report in Excel format
- **Authentication**: Required (School Admin only)
- **Request Body**:
```json
{
    "start_date": "2024-12-01",
    "end_date": "2024-12-31",
    "fee_type": "TUITION",
    "class_id": 1,
    "section_id": null,
    "payment_status": "PAID"
}
```
- **Response**: Excel file download with fee report

## 8. Subjects API (/subjects)

### 8.1. Create Subject
- **Endpoint**: `/subjects`
- **Method**: POST
- **Description**: Create a new subject
- **Authentication**: Required
- **Request Body**:
```json
{
    "name": "Mathematics",
    "code": "MATH101",
    "description": "Basic Mathematics",
    "credits": 5,
    "tenant_id": 1,
    "school_id": 1,
    "is_active": true
}
```
- **Response**:
```json
{
    "name": "Mathematics",
    "code": "MATH101",
    "description": "Basic Mathematics",
    "credits": 5,
    "is_active": true,
    "id": 1,
    "school_id": 1,
    "created_at": "2024-12-18T10:41:17.342373+00:00",
    "updated_at": "2024-12-18T10:41:17.342373+00:00"
}
```

### 8.2. List Subjects
- **Endpoint**: `/subjects`
- **Method**: GET
- **Description**: List subjects
- **Authentication**: Required
- **Query Parameters**:
  - skip: int (optional, default: 0)
  - limit: int (optional, default: 100, max: 100)
  - is_active: boolean (optional) - Filter by active status
- **Response**: List of subjects

### 8.3. Get Subject
- **Endpoint**: `/subjects/{subject_id}`
- **Method**: GET
- **Description**: Get subject by ID
- **Authentication**: Required
- **Response**: Subject details

### 8.4. Update Subject
- **Endpoint**: `/subjects/{subject_id}`
- **Method**: PUT
- **Description**: Update subject
- **Authentication**: Required
- **Request Body**: Same as create (all fields optional)
- **Response**: Updated subject

## 9. Timetable API (/academic/timetables)

### 9.1. Create Timetable
- **Endpoint**: `/academic/timetables`
- **Method**: POST
- **Description**: Create a new timetable (School Admin only)
- **Authentication**: Required
- **Request Body**:
```json
{
    "name": "Class 1 Timetable",
    "academic_year_id": 1,
    "class_id": 1,
    "section_id": 1,
    "tenant_id": 1,
    "school_id": 1,
    "effective_from": "2024-04-01",
    "is_active": true
}
```
- **Response**: Created timetable

### 9.2. List Timetables
- **Endpoint**: `/academic/timetables`
- **Method**: GET
- **Description**: List timetables
- **Authentication**: Required
- **Query Parameters**:
  - academic_year_id: int (optional) - Filter by academic year
  - is_active: boolean (optional) - Filter by active status
  - skip: int (optional, default: 0)
  - limit: int (optional, default: 100, max: 100)
- **Response**: List of timetables

### 9.3. Get Timetable
- **Endpoint**: `/academic/timetables/{timetable_id}`
- **Method**: GET
- **Description**: Get timetable by ID
- **Authentication**: Required
- **Response**: Timetable details

### 9.4. Update Timetable
- **Endpoint**: `/academic/timetables/{timetable_id}`
- **Method**: PUT
- **Description**: Update timetable (School Admin only)
- **Authentication**: Required
- **Request Body**: Same as create (all fields optional)
- **Response**: Updated timetable

### 9.5. Create Period
- **Endpoint**: `/academic/timetables/{timetable_id}/periods`
- **Method**: POST
- **Description**: Create a new period in a timetable (School Admin only)
- **Authentication**: Required
- **Request Body**:
```json
{
    "timetable_id": 1,
    "day_of_week": "MONDAY",
    "period_number": 1,
    "start_time": "09:00:00",
    "end_time": "09:45:00",
    "subject_id": 1,
    "teacher_id": 1,
    "room": "101",
    "is_break": false
}
```
- **Response**: Created period

### 9.6. List Periods
- **Endpoint**: `/academic/timetables/{timetable_id}/periods`
- **Method**: GET
- **Description**: List periods in a timetable
- **Authentication**: Required
- **Query Parameters**:
  - skip: int (optional, default: 0)
  - limit: int (optional, default: 100, max: 100)
- **Response**: List of periods

### 9.7. Get Period
- **Endpoint**: `/academic/timetables/{timetable_id}/periods/{period_id}`
- **Method**: GET
- **Description**: Get period by ID
- **Authentication**: Required
- **Response**: Period details

### 9.8. Update Period
- **Endpoint**: `/academic/timetables/{timetable_id}/periods/{period_id}`
- **Method**: PUT
- **Description**: Update period (School Admin only)
- **Authentication**: Required
- **Request Body**: Same as create period (all fields optional)
- **Response**: Updated period
```