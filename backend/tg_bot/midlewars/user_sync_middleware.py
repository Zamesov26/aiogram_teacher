import logging
from aiogram import BaseMiddleware
from aiogram.types import Update, User
from typing import Callable, Awaitable, Any, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.database.models import TelegramUser

logger = logging.getLogger(__name__)


class UserSyncMiddleware(BaseMiddleware):
    """Middleware для синхронизации пользователей Telegram с базой."""

    def __init__(self, session_factory: Callable[[], AsyncSession]):
        super().__init__()
        self.session_factory = session_factory

    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any],
    ) -> Any:
        tg_user: User | None = None

        # Извлекаем пользователя из апдейта
        if event.message:
            tg_user = event.message.from_user
        elif event.callback_query:
            tg_user = event.callback_query.from_user
        elif event.inline_query:
            tg_user = event.inline_query.from_user

        if tg_user:
            async with self.session_factory() as session:
                user = await session.scalar(select(TelegramUser).where(TelegramUser.id == tg_user.id))
                if not user:
                    user = TelegramUser(
                        id=tg_user.id,
                        is_bot=tg_user.is_bot,
                        first_name=tg_user.first_name,
                        last_name=tg_user.last_name,
                        username=tg_user.username,
                        language_code=tg_user.language_code,
                    )
                    session.add(user)
                    logger.info(f"👤 Новый пользователь добавлен: {tg_user.username or tg_user.id}")
                else:
                    user.updated_at = user.updated_at  # вызовет onupdate
                await session.commit()

        return await handler(event, data)
