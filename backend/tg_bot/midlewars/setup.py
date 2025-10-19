import typing

from backend.tg_bot.midlewars.db_session_factory_middleware import DBSessionMiddleware
from backend.tg_bot.midlewars.error_handler import ErrorHandlerMiddleware
from backend.tg_bot.midlewars.logger import LoggingMiddleware

if typing.TYPE_CHECKING:
    from aiogram import Dispatcher


def setup_middlewares(dp: "Dispatcher", session_factory) -> None:
    """Подключает все middleware проекта."""
    dp.update.middleware(LoggingMiddleware())
    dp.update.middleware(DBSessionMiddleware(session_factory))
    dp.update.middleware(ErrorHandlerMiddleware())
