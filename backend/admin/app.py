from fastapi import FastAPI
from sqladmin import Admin, ModelView
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from sqlalchemy import select
from backend.database.engine import db_session_factory, engine
from backend.database.models import Lesson, Task, Teacher, TGAdmin as AdminModel
from passlib.hash import bcrypt


class DatabaseAuth(AuthenticationBackend):
    """Авторизация через таблицу Admin в БД."""

    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = form.get("username")
        password = form.get("password")

        async with db_session_factory() as session:
            db_admin = await session.scalar(
                select(AdminModel).where(AdminModel.username == username)
            )

            if (
                db_admin
                # and db_admin.is_active
                and bcrypt.verify(password, db_admin.password)
            ):
                request.session.update({"user": db_admin.username})
                return True

        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request):
        return request.session.get("user")

# 🔹 Регистрируем модели
class LessonAdmin(ModelView, model=Lesson):
    column_list = [Lesson.id, Lesson.title, Lesson.created_at]


class TaskAdmin(ModelView, model=Task):
    column_list = [Task.id, Task.text, Task.is_active]


class TeacherAdmin(ModelView, model=Teacher):
    column_list = [Teacher.id, Teacher.user_id, Teacher.subject, Teacher.is_active]


