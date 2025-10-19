from aiogram import BaseMiddleware
from aiogram.types import Update
from typing import Callable, Dict, Any, Awaitable

from backend.services.exceptions.link_exceptions import (
    LinkError,
    InvalidLinkError,
    GroupNotFoundError,
    AlreadyInGroupError,
    GroupJoinError,
)


class ErrorHandlerMiddleware(BaseMiddleware):
    """Перехватывает бизнес-исключения и отправляет сообщения пользователю."""

    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any],
    ) -> Any:
        try:
            return await handler(event, data)

        except InvalidLinkError:
            await self._send_message(event, "⚠️ Неверная или устаревшая ссылка.")

        except GroupNotFoundError:
            await self._send_message(event, "❌ Группа не найдена или неактивна.")

        except AlreadyInGroupError:
            await self._send_message(event, "ℹ️ Вы уже состоите в этой группе.")

        except GroupJoinError:
            await self._send_message(
                event, "🚫 Ошибка при добавлении в группу. Попробуйте позже."
            )

        except LinkError:
            await self._send_message(event, "⚠️ Произошла ошибка при обработке ссылки.")

        except Exception as e:
            # Логируем все неожиданные ошибки, но не показываем пользователю детали
            print(f"⚠️ Unhandled error: {e!r}")
            await self._send_message(
                event, "😞 Произошла непредвиденная ошибка. Попробуйте позже."
            )

    async def _send_message(self, event: Update, text: str):
        """Отправка сообщения пользователю, независимо от типа апдейта."""
        if getattr(event, "message", None):
            await event.message.answer(text)
        elif getattr(event, "callback_query", None):
            await event.callback_query.message.answer(text)
        elif getattr(event, "inline_query", None):
            # inline-query не поддерживает обычные ответы
            pass
