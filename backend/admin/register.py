from sqladmin import Admin

from backend.admin.admin import LessonAdmin, TaskAdmin, TeacherAdmin
from backend.admin.auth import DatabaseAuth


def init_admin(app, engine, secret_key="super_secret_key"):
    auth_backend = DatabaseAuth(secret_key=secret_key)
    admin = Admin(app, engine, authentication_backend=auth_backend)

    # admin.add_view(LessonAdmin)
    # admin.add_view(TaskAdmin)
    # admin.add_view(TeacherAdmin)
    return admin
