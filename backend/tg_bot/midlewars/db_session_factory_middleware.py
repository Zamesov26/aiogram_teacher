from aiogram import BaseMiddleware
from typing import Callable, Awaitable, Any, Dict


class DBSessionMiddleware(BaseMiddleware):
    def __init__(self, session_factory):
        super().__init__()
        self.session_factory = session_factory

    async def __call__(
        self,
        handler: Callable[[Any, Dict[str, Any]], Awaitable[Any]],
        event: Any,
        data: Dict[str, Any],
    ):
        data["session_factory"] = self.session_factory
        return await handler(event, data)
