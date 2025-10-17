__all__ = [
    "TelegramUser",
    "Teacher",
    "TGAdmin",
    "Task",
    "Lesson",
]

from backend.database.models.task import Task, Lesson
from backend.database.models.teacher import Teacher
from backend.database.models.tg_admin import TGAdmin
from backend.database.models.users import TelegramUser
