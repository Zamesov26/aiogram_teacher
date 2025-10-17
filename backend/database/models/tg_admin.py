import typing
from datetime import datetime

from sqlalchemy import BigInteger, ForeignKey, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, backref, relationship

if typing.TYPE_CHECKING:
    from backend.database.models import TelegramUser
from backend.database.models.base import Base


class TGAdmin(Base):
    """Администратор бота."""

    __tablename__ = "admins"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("telegram_users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    username: Mapped[str] = mapped_column(String(64), unique=True, nullable=True)
    password: Mapped[str] = mapped_column(String(128), nullable=True)  # хэш пароля
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped["TelegramUser"] = relationship(
        "TelegramUser", backref=backref("admin", uselist=False)
    )
