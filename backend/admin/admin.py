from sqladmin import ModelView

from backend.database.models import Lesson, Task, Teacher


class LessonAdmin(ModelView, model=Lesson):
    column_list = [Lesson.id, Lesson.title, Lesson.created_at]


class TaskAdmin(ModelView, model=Task):
    column_list = [Task.id, Task.text, Task.is_active]


class TeacherAdmin(ModelView, model=Teacher):
    column_list = [Teacher.id, Teacher.user_id, Teacher.subject, Teacher.is_active]
