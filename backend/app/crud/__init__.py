from app.crud.tenant import (
    create_tenant,
    get_tenant,
    get_tenants,
    update_tenant,
    delete_tenant
)
from app.crud.school import (
    create_school,
    get_school,
    get_schools,
    update_school,
    delete_school
)
from app.crud.user import (
    create_user,
    get_user,
    get_users,
    update_user,
    delete_user,
    get_user_by_email,
    get_user_by_username
)
from app.crud.academic import (
    create_academic_year,
    get_academic_year,
    get_academic_years,
    update_academic_year,
    create_class,
    get_class,
    get_classes,
    update_class,
    create_section,
    get_section,
    get_sections,
    update_section,
    create_subject,
    get_subject,
    get_subjects,
    update_subject,
    assign_student_to_section,
    assign_teacher_to_section,
    get_class_students,
    get_teacher_classes
)

__all__ = [
    # Tenant
    "create_tenant",
    "get_tenant",
    "get_tenants",
    "update_tenant",
    "delete_tenant",
    # School
    "create_school",
    "get_school",
    "get_schools",
    "update_school",
    "delete_school",
    # User
    "create_user",
    "get_user",
    "get_users",
    "update_user",
    "delete_user",
    "get_user_by_email",
    "get_user_by_username",
    # Academic
    "create_academic_year",
    "get_academic_year",
    "get_academic_years",
    "update_academic_year",
    "create_class",
    "get_class",
    "get_classes",
    "update_class",
    "create_section",
    "get_section",
    "get_sections",
    "update_section",
    "create_subject",
    "get_subject",
    "get_subjects",
    "update_subject",
    "assign_student_to_section",
    "assign_teacher_to_section",
    "get_class_students",
    "get_teacher_classes"
]