from datetime import datetime, UTC
from typing import TYPE_CHECKING

from sqlalchemy import Table, Column, ForeignKey, Float, DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from backend.database.models import Course, Task, GroupLesson
from backend.database.models.associations import lesson_tasks
from backend.database.models.base import Base

lesson_progress = Table(
    "lesson_progress",
    Base.metadata,
    Column("lesson_id", ForeignKey("lessons.id", ondelete="CASCADE"), primary_key=True),
    Column(
        "user_id", ForeignKey("telegram_users.id", ondelete="CASCADE"), primary_key=True
    ),
    Column("progress", Float, default=0.0),
    Column(
        "updated_at",
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    ),
)


class Lesson(Base):
    """Урок, содержащий задачи."""

    __tablename__ = "lessons"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    course_id: Mapped[int] = mapped_column(
        ForeignKey("courses.id", ondelete="CASCADE"), nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now(UTC)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now(UTC), onupdate=datetime.now(UTC)
    )

    tasks: Mapped[list["Task"]] = relationship(
        "Task",
        secondary=lesson_tasks,
        back_populates="lessons",
    )
    course: Mapped["Course"] = relationship(
        "Course",
        back_populates="lessons",
    )
    group_access: Mapped[list["GroupLesson"]] = relationship(
        "GroupLesson", back_populates="lesson", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"{self.id}:{self.title}"
