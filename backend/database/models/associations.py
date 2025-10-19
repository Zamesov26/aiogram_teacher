from sqlalchemy import Table, Column, ForeignKey

from backend.database.models.base import Base

lesson_tasks = Table(
    "lesson_tasks",
    Base.metadata,
    Column("lesson_id", ForeignKey("lessons.id", ondelete="CASCADE"), primary_key=True),
    Column("task_id", ForeignKey("tasks.id", ondelete="CASCADE"), primary_key=True),
)
