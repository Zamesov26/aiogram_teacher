from aiogram import BaseMiddleware
from typing import Callable, Awaitable, Any, Dict


class DBSessionMiddleware(BaseMiddleware):
    """Создаёт AsyncSession и передаёт его в handler через data."""

    def __init__(self, session_factory):
        super().__init__()
        self.session_factory = session_factory

    async def __call__(
        self,
        handler: Callable[[Any, Dict[str, Any]], Awaitable[Any]],
        event: Any,
        data: Dict[str, Any],
    ) -> Any:
        async with self.session_factory() as session:
            data["db_session"] = session
            result = await handler(event, data)
            await session.commit()
            return result
