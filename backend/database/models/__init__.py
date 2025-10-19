__all__ = [
    "Teacher",
    "TGAdmin",
    "LinkEvent",
    "Course",
    "Lesson",
    "Task",
    "Group",
    "TelegramUser",
    "GroupLesson",
    "TaskProgress",
]

from backend.database.models.group import Group, GroupLesson
from backend.database.models.link_event import LinkEvent
from backend.database.models.course import Task, Lesson, Course, TaskProgress
from backend.database.models.teacher import Teacher
from backend.database.models.tg_admin import TGAdmin
from backend.database.models.users import TelegramUser
from backend.database.models.course import Course
