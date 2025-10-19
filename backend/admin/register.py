from sqladmin import Admin

from backend.admin.admin import (
    LessonAdmin,
    TaskAdmin,
    TeacherAdmin,
    GroupAdmin,
    CourseAdmin,
    UserAdmin,
)
from backend.admin.auth import DatabaseAuth


def init_admin(app, engine, secret_key="super_secret_key"):
    auth_backend = DatabaseAuth(secret_key=secret_key)
    admin = Admin(app, engine, authentication_backend=auth_backend)

    admin.add_view(UserAdmin)
    admin.add_view(TeacherAdmin)
    admin.add_view(GroupAdmin)

    admin.add_view(CourseAdmin)
    admin.add_view(LessonAdmin)
    admin.add_view(TaskAdmin)
    return admin
