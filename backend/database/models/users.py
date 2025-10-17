from datetime import datetime

from sqlalchemy import BigInteger, Boolean, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from backend.database.models.base import Base


class TelegramUser(Base):
    """Пользователь Telegram."""

    __tablename__ = "telegram_users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=False)
    # Telegram ID — большой int, не автоинкрементный

    is_bot: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    first_name: Mapped[str] = mapped_column(String(64), nullable=True)
    last_name: Mapped[str] = mapped_column(String(64), nullable=True)
    username: Mapped[str] = mapped_column(String(64), nullable=True, index=True)
    language_code: Mapped[str] = mapped_column(String(8), nullable=True)

    # дополнительные поля
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
