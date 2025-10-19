from sqladmin import ModelView

from backend.database.models import Lesson, Task, Teacher, Group, Course, TelegramUser


class UserAdmin(ModelView, model=TelegramUser):
    name = "Пользователь"
    name_plural = "Пользователи"
    column_list = "__all__"


class GroupAdmin(ModelView, model=Group):
    name = "Группа"
    name_plural = "Группы"
    column_list = "__all__"


class TeacherAdmin(ModelView, model=Teacher):
    name = "Учитель"
    name_plural = "Учителя"
    column_list = "__all__"


class CourseAdmin(ModelView, model=Course):
    category = "Обучение"
    name = "Курс"
    name_plural = "Курсы"
    column_list = "__all__"


class LessonAdmin(ModelView, model=Lesson):
    category = "Обучение"
    name = "Урок"
    name_plural = "Уроки"
    column_list = "__all__"


class TaskAdmin(ModelView, model=Task):
    category = "Обучение"
    name = "Задача"
    name_plural = "Задачи"
    column_list = "__all__"
