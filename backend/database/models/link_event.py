from datetime import datetime, UTC
from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, DateTime, Enum, ForeignKey, JSON, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum as PyEnum

if TYPE_CHECKING:
    from backend.database.models import TelegramUser
from backend.database.models.base import Base


class LinkType(str, PyEnum):
    REFERRAL = "referral"
    COURSE_INVITE = "course_invite"
    TEACHER_INVITE = "teacher_invite"
    PROMO = "promo"


class LinkEvent(Base):
    """Универсальная модель для ссылок с параметрами (рефералы, приглашения и т.д.)."""

    __tablename__ = "link_events"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    type: Mapped[LinkType] = mapped_column(Enum(LinkType), nullable=False)
    creator_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("telegram_users.id", ondelete="SET NULL"),
        nullable=True,
    )
    payload: Mapped[dict] = mapped_column(JSON, default=dict)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_one_time: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now(UTC)
    )
    expires_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    creator: Mapped["TelegramUser"] = relationship(
        "TelegramUser", backref="link_events"
    )

    def __repr__(self) -> str:
        return (
            f"<LinkEvent(code='{self.code}', type='{self.type}', "
            f"creator_id={self.creator_id}, is_active={self.is_active})>"
        )
