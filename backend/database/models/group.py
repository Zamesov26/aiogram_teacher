from datetime import datetime, UTC
from typing import Optional, TYPE_CHECKING

from sqlalchemy import (
    ForeignKey,
    String,
    Text,
    Integer,
    Boolean,
    DateTime,
    Column,
    Table,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship, backref

from backend.database.models.base import Base

if TYPE_CHECKING:
    from backend.database.models.course import Course
    from backend.database.models import TelegramUser


group_users = Table(
    "group_users",
    Base.metadata,
    Column(
        "group_id",
        ForeignKey("groups.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "user_id",
        ForeignKey("telegram_users.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "joined_at",
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    ),
    Column(
        "role",
        String(32),
        default="student",  # варианты: student | teacher | assistant
        nullable=False,
    ),
)


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    course_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("courses.id", ondelete="SET NULL")
    )
    teacher_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("telegram_users.id", ondelete="SET NULL")
    )

    title: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    chat_id: Mapped[Optional[int]] = mapped_column(
        Integer
    )  # если будет Telegram-группа
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    start_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    end_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )

    # связи
    course: Mapped[Optional["Course"]] = relationship(
        "Course", backref=backref("groups")
    )
    teacher: Mapped[Optional["TelegramUser"]] = relationship(
        "TelegramUser", backref=backref("teaching_groups")
    )

    users: Mapped[list["TelegramUser"]] = relationship(
        "TelegramUser",
        secondary="group_users",
        back_populates="groups",
    )
