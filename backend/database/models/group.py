from datetime import datetime, UTC
from typing import Optional, TYPE_CHECKING

from sqlalchemy import (
    ForeignKey,
    String,
    Text,
    Integer,
    Boolean,
    DateTime,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship, backref

from backend.database.models.base import Base

if TYPE_CHECKING:
    from backend.database.models.course import Course
    from backend.database.models import TelegramUser, Lesson, LinkEvent


class GroupUser(Base):
    """Участник группы (M2M между Group и TelegramUser)."""

    __tablename__ = "group_users"

    group_id: Mapped[int] = mapped_column(
        ForeignKey("groups.id", ondelete="CASCADE"),
        primary_key=True,
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("telegram_users.id", ondelete="CASCADE"),
        primary_key=True,
    )

    joined_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    role: Mapped[str] = mapped_column(
        String(32),
        default="student",  # варианты: student | teacher | assistant
        nullable=False,
    )

    link_event_id: Mapped[int | None] = mapped_column(
        ForeignKey("link_events.id", ondelete="SET NULL"),
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Связи
    group: Mapped["Group"] = relationship("Group", back_populates="members")
    user: Mapped["TelegramUser"] = relationship(
        "TelegramUser", back_populates="group_memberships"
    )

    link_event: Mapped["LinkEvent"] = relationship("LinkEvent")


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
    members: Mapped[list["GroupUser"]] = relationship(
        "GroupUser", back_populates="group", cascade="all, delete-orphan"
    )
    lesson_access: Mapped[list["GroupLesson"]] = relationship(
        "GroupLesson", back_populates="group", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"{self.title}"


class GroupLesson(Base):
    """Статус доступности урока для конкретной группы."""

    __tablename__ = "group_lessons"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    group_id: Mapped[int] = mapped_column(
        ForeignKey("groups.id", ondelete="CASCADE"),
        nullable=False,
    )
    lesson_id: Mapped[int] = mapped_column(
        ForeignKey("lessons.id", ondelete="CASCADE"),
        nullable=False,
    )

    is_open: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    opened_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    closed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    # Если хочешь фиксировать, кто открыл (например, учитель)
    opened_by_id: Mapped[int | None] = mapped_column(
        ForeignKey("telegram_users.id", ondelete="SET NULL")
    )

    __table_args__ = (
        UniqueConstraint("group_id", "lesson_id", name="uq_group_lesson_access"),
    )

    # ORM-связи
    group: Mapped["Group"] = relationship("Group", back_populates="lesson_access")
    lesson: Mapped["Lesson"] = relationship("Lesson", back_populates="group_access")
    opened_by: Mapped["TelegramUser"] = relationship("TelegramUser")
