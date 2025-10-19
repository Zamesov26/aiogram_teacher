from datetime import datetime, UTC
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Text, String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from backend.database.models import Lesson
from backend.database.models.associations import lesson_tasks
from backend.database.models.base import Base


class Task(Base):
    """Задача, связанная с уроками."""

    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    image_url: Mapped[str] = mapped_column(String(255), nullable=True)
    test_data: Mapped[str] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now(UTC)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now(UTC), onupdate=datetime.now(UTC)
    )

    lessons: Mapped[list["Lesson"]] = relationship(
        "Lesson",
        secondary=lesson_tasks,
        back_populates="tasks",
    )

    def __repr__(self):
        return f"{self.id}:{self.text}"


class TaskProgress(Base):
    """Прогресс выполнения задач учеником."""

    __tablename__ = "task_progress"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("telegram_users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    task_id: Mapped[int] = mapped_column(
        ForeignKey("tasks.id", ondelete="CASCADE"),
        primary_key=True,
    )
    lesson_id: Mapped[int] = mapped_column(
        ForeignKey("lessons.id", ondelete="CASCADE"),
        nullable=False,
    )
    group_id: Mapped[int] = mapped_column(
        ForeignKey("groups.id", ondelete="CASCADE"), nullable=False
    )

    # TODO Enum
    status: Mapped[str] = mapped_column(
        String(15),
        default="pending",  # pending / done / failed
        nullable=False,
    )

    is_checked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )

    user = relationship("TelegramUser", backref="task_progress")
    task = relationship("Task", backref="progress")
    lesson = relationship("Lesson", backref="task_progress")
    group = relationship("Group", backref="task_progress")
