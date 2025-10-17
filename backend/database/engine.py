from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from backend.settings import Settings

settings = Settings()
engine = create_async_engine(settings.db.url)
db_session_factory = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)
