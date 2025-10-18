from passlib.hash import bcrypt
from sqladmin.authentication import AuthenticationBackend
from sqlalchemy import select
from starlette.requests import Request

from backend.database.engine import db_session_factory
from backend.database.models import TGAdmin as AdminModel


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
