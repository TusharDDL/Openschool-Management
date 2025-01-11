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

class WeekDay(str, Enum):
    MONDAY = "MONDAY"
    TUESDAY = "TUESDAY"
    WEDNESDAY = "WEDNESDAY"
    THURSDAY = "THURSDAY"
    FRIDAY = "FRIDAY"
    SATURDAY = "SATURDAY"
    SUNDAY = "SUNDAY"

class GradingSystem(str, Enum):
    PERCENTAGE = "PERCENTAGE"
    LETTER = "LETTER"
    GPA = "GPA"
    CUSTOM = "CUSTOM"

class AssessmentType(str, Enum):
    QUIZ = "QUIZ"
    TEST = "TEST"
    EXAM = "EXAM"
    ASSIGNMENT = "ASSIGNMENT"
    PROJECT = "PROJECT"
    PRESENTATION = "PRESENTATION"
    LAB = "LAB"
    OTHER = "OTHER"