from datetime import datetime, UTC
from typing import Optional

from sqlalchemy import BigInteger, Boolean, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

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
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now(UTC)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now(UTC), onupdate=datetime.now(UTC)
    )

    admin: Mapped[Optional["TGAdmin"]] = relationship(
        "TGAdmin",
        back_populates="user",
        uselist=False,
    )
    teacher: Mapped[Optional["Teacher"]] = relationship(
        "Teacher", back_populates="user", uselist=False
    )
    groups: Mapped[list["Group"]] = relationship(
        "Group",
        secondary="group_users",
        back_populates="users",
    )
