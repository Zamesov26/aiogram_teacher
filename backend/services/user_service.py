from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database.models import TelegramUser


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_or_create_user(self, tg_user) -> tuple[TelegramUser, bool]:
        user = await self.session.scalar(
            select(TelegramUser).where(TelegramUser.id == tg_user.id)
        )
        if not user:
            user = TelegramUser(
                id=tg_user.id,
                is_bot=tg_user.is_bot,
                first_name=tg_user.first_name,
                last_name=tg_user.last_name,
                username=tg_user.username,
                language_code=tg_user.language_code,
            )
            self.session.add(user)
            await self.session.commit()
            return user, True
        return user, False
