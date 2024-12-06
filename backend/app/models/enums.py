from enum import Enum

class UserRole(str, Enum):
    SUPER_ADMIN = "SUPER_ADMIN"
    SCHOOL_ADMIN = "SCHOOL_ADMIN"
    TEACHER = "TEACHER"
    STUDENT = "STUDENT"
    PARENT = "PARENT"

# Role hierarchy for permission checking
ROLE_HIERARCHY = {
    UserRole.SUPER_ADMIN: 100,
    UserRole.SCHOOL_ADMIN: 80,
    UserRole.TEACHER: 60,
    UserRole.STUDENT: 40,
    UserRole.PARENT: 20
}