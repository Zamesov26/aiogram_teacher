from datetime import datetime, UTC
from typing import Optional

from sqlalchemy import String, Text, Boolean, DateTime, ForeignKey, Table, Column, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )

    lessons: Mapped[list["Lesson"]] = relationship(
        "Lesson",
        back_populates="course",
        cascade="all, delete-orphan",
    )


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


lesson_tasks = Table(
    "lesson_tasks",
    Base.metadata,
    Column("lesson_id", ForeignKey("lessons.id", ondelete="CASCADE"), primary_key=True),
    Column("task_id", ForeignKey("tasks.id", ondelete="CASCADE"), primary_key=True),
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


class Task(Base):
    """Задача, связанная с уроками."""

    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    image_url: Mapped[str] = mapped_column(String(256), nullable=True)
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
