from fastapi.openapi.utils import get_openapi
from app.core.config import settings

def custom_openapi(app):
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="School Management System API",
        version="1.0.0",
        description="""
        School Management System API documentation.
        
        ## Authentication
        Most endpoints require authentication using JWT Bearer token.
        
        ## Rate Limiting
        API endpoints are rate-limited to prevent abuse.
        
        ## Error Codes
        - 400: Bad Request
        - 401: Unauthorized
        - 403: Forbidden
        - 404: Not Found
        - 422: Validation Error
        - 429: Too Many Requests
        - 500: Internal Server Error
        """,
        routes=app.routes,
    )

    # Add security scheme
    openapi_schema["components"]["securitySchemes"] = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    # Add global security requirement
    openapi_schema["security"] = [{"bearerAuth": []}]

    # Add response examples
    openapi_schema["components"]["examples"] = {
        "UserResponse": {
            "value": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "email": "user@example.com",
                "full_name": "John Doe",
                "role": "teacher",
                "is_active": True,
            }
        },
        "ErrorResponse": {
            "value": {
                "detail": "Error message",
                "type": "validation_error",
            }
        },
    }

    # Add tags metadata
    openapi_schema["tags"] = [
        {
            "name": "auth",
            "description": "Authentication operations",
        },
        {
            "name": "users",
            "description": "User management operations",
        },
        {
            "name": "schools",
            "description": "School management operations",
        },
        {
            "name": "students",
            "description": "Student management operations",
        },
        {
            "name": "teachers",
            "description": "Teacher management operations",
        },
        {
            "name": "courses",
            "description": "Course management operations",
        },
        {
            "name": "attendance",
            "description": "Attendance management operations",
        },
        {
            "name": "grades",
            "description": "Grade management operations",
        },
    ]

    app.openapi_schema = openapi_schema
    return app.openapi_schema