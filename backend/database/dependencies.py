from sqlalchemy.ext.asyncio import AsyncSession
from backend.database.engine import db_session_factory


async def get_session() -> AsyncSession:
    """Зависимость FastAPI для получения асинхронной сессии."""
    async with db_session_factory() as session:
        yield session
