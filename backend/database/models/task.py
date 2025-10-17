from datetime import datetime

from sqlalchemy import String, Text, Boolean, DateTime, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

lesson_tasks = Table(
    "lesson_tasks",
    Base.metadata,
    Column("lesson_id", ForeignKey("lessons.id", ondelete="CASCADE"), primary_key=True),
    Column("task_id", ForeignKey("tasks.id", ondelete="CASCADE"), primary_key=True),
)


class Task(Base):
    """Задача, связанная с уроками."""

    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    image_url: Mapped[str] = mapped_column(String(256), nullable=True)
    test_data: Mapped[str] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    lessons: Mapped[list["Lesson"]] = relationship(
        "Lesson",
        secondary=lesson_tasks,
        back_populates="tasks",
    )


class Lesson(Base):
    """Урок, содержащий задачи."""

    __tablename__ = "lessons"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    tasks: Mapped[list[Task]] = relationship(
        "Task",
        secondary=lesson_tasks,
        back_populates="lessons",
    )
