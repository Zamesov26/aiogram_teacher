import typing

from backend.tg_bot.midlewars.db_session_middleware import DBSessionMiddleware
from backend.tg_bot.midlewars.logger import LoggingMiddleware
from backend.tg_bot.midlewars.user_sync_middleware import UserSyncMiddleware

if typing.TYPE_CHECKING:
    from aiogram import Dispatcher


def setup_middlewares(dp: "Dispatcher", session_factory) -> None:
    """Подключает все middleware проекта."""
    dp.update.middleware(LoggingMiddleware())
    dp.update.middleware(DBSessionMiddleware(session_factory))
    dp.update.middleware(UserSyncMiddleware())
