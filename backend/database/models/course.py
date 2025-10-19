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

    def __repr__(self):
        return f"{self.id}:{self.title}"


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
    group_access: Mapped[list["GroupLesson"]] = relationship(
        "GroupLesson", back_populates="lesson", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"{self.id}:{self.title}"


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

    status: Mapped[str] = mapped_column(
        String(16),
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
