import logging
from aiogram import BaseMiddleware
from aiogram.types import Update
from typing import Callable, Awaitable, Any, Dict

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger("update_logger")


class LoggingMiddleware(BaseMiddleware):
    """Middleware для логирования всех апдейтов."""

    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any],
    ) -> Any:
        try:
            # Здесь можно добавить фильтрацию по типу апдейта
            logger.info(f"📩 Received update: {event.model_dump_json(indent=2)}")
        except Exception as e:
            logger.warning(f"Ошибка при логировании апдейта: {e}")

        result = await handler(event, data)
        return result
