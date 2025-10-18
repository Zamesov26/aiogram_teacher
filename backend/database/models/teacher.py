import typing
from datetime import datetime, UTC

from sqlalchemy import String, Boolean, BigInteger, DateTime, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship, backref


if typing.TYPE_CHECKING:
    from backend.database.models import TelegramUser
from backend.database.models.base import Base


class Teacher(Base):
    """Учитель, связанный с Telegram-пользователем."""

    __tablename__ = "teachers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("telegram_users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )

    subject: Mapped[str] = mapped_column(String(64), nullable=True)
    bio: Mapped[str] = mapped_column(String(256), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now(UTC)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now(UTC), onupdate=datetime.now(UTC)
    )

    user: Mapped["TelegramUser"] = relationship(
        "TelegramUser", back_populates="teacher", uselist=False
    )
