from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.orm import raiseload, joinedload

from backend.database.dao import TeacherDAO
from backend.database.models import Group, Lesson, GroupLesson, TaskProgress
from backend.database.models.group import GroupUser
from backend.services.assignments_service import AssignmentsService
from backend.services.link_service import LinkService

router = Router()


@router.callback_query(F.data == "teacher_groups")
async def handle_teacher_menu(
    callback: CallbackQuery, session_factory: async_sessionmaker[AsyncSession]
):
    async with session_factory() as session:
        groups = await session.scalars(
            select(Group)
            .where(Group.teacher_id == callback.from_user.id, Group.is_active)
            .options(
                raiseload("*"),
            )
        )

        kb = InlineKeyboardBuilder()
        for group in groups:
            kb.button(text=f"{group.title}", callback_data=f"group_menu:{group.id}")
        kb.adjust(1)
        await callback.message.answer("Выберите группу", reply_markup=kb.as_markup())


@router.callback_query(F.data.startswith("group_menu:"))
async def handle_group_menu(
    callback: CallbackQuery, session_factory: async_sessionmaker[AsyncSession]
):
    group_id = int(callback.data.split(":")[1])
    async with session_factory() as session:
        if not await TeacherDAO(session).has_access_to_group(
            teacher_id=callback.from_user.id, group_id=group_id
        ):
            return

    kb = InlineKeyboardBuilder()
    kb.button(text=f"Управление уроками", callback_data=f"lessons:{group_id}")
    kb.button(text=f"Получить ссылку", callback_data=f"generate_link:{group_id}")
    kb.adjust(1)
    await callback.message.answer("Выберите действие", reply_markup=kb.as_markup())


@router.callback_query(F.data.startswith("generate_link:"))
async def handle_group_link(
    callback: CallbackQuery, session_factory: async_sessionmaker[AsyncSession]
):
    group_id = int(callback.data.split(":")[1])
    async with session_factory() as session:
        if not await TeacherDAO(session).has_access_to_group(
            teacher_id=callback.from_user.id, group_id=group_id
        ):
            return

        link = await LinkService(session).create_group_invite_code(
            creator_id=callback.from_user.id, group_id=group_id
        )
        pass
    await callback.message.answer(
        f"Ссылка добавления в группу:\n"
        f"https://t.me/skill_growth_bot?start={link.code}"
    )


@router.callback_query(F.data.startswith("lessons:"))
async def handle_group_lesson_list(
    callback: CallbackQuery, session_factory: async_sessionmaker[AsyncSession]
):
    group_id = int(callback.data.split(":")[1])
    async with session_factory() as session:
        if not await TeacherDAO(session).has_access_to_group(
            teacher_id=callback.from_user.id, group_id=group_id
        ):
            return

        lessons_query = (
            select(Lesson.id, Lesson.title, GroupLesson.is_open)
            .join(Group, Group.course_id == Lesson.course_id)
            .outerjoin(
                GroupLesson,
                (GroupLesson.lesson_id == Lesson.id)
                & (GroupLesson.group_id == group_id),
            )
            .where(Group.id == group_id)
            .order_by(Lesson.id)
        )

        result = await session.execute(lessons_query)
        lessons = result.all()

        if not lessons:
            await callback.message.answer("ℹ️ В этом курсе пока нет уроков.")
            return

        kb = InlineKeyboardBuilder()
        for lesson_id, title, is_open in lessons:
            if is_open:
                kb.button(
                    text=f"🔓 Закрыть: {title}",
                    callback_data=f"lesson_close:{group_id}:{lesson_id}",
                )
            else:
                kb.button(
                    text=f"🔒 Открыть: {title}",
                    callback_data=f"lesson_open:{group_id}:{lesson_id}",
                )

        kb.adjust(1)
        await callback.message.answer(
            f"📚 Уроки для группы #{group_id}",
            reply_markup=kb.as_markup(),
        )


@router.callback_query(F.data.startswith("lesson_open:"))
async def handle_group_open_lesson(
    callback: CallbackQuery, session_factory: async_sessionmaker[AsyncSession], bot
):
    group_id, lesson_id = map(int, callback.data.split(":")[1:])
    async with session_factory() as session:
        if not await TeacherDAO(session).has_access_to_group(
            teacher_id=callback.from_user.id, group_id=group_id
        ):
            return
        
        gl = await AssignmentsService(session).open_lesson_for_group(
            group_id=group_id, lesson_id=lesson_id, teacher_id=callback.from_user.id
        )
        if not gl:
            return

        # TODO перенести ниже после создание прогресса по задачам

        # Получаем сам урок и его задачи
        lesson = await session.scalar(
            select(Lesson)
            .where(Lesson.id == lesson_id)
            .options(joinedload(Lesson.tasks))
        )
        # Получаем группу
        group = await session.scalar(select(Group).where(Group.id == group_id))

        # получаем студентов для оповещения
        student_ids = await session.scalars(
            select(GroupUser.user_id).where(
                GroupUser.group_id == group_id,
                GroupUser.role == "student",
                GroupUser.is_active.is_(True),
            )
        )
        student_ids = list(student_ids)

        # TODO нужно вынести в отдельную таску
        # Проходим по всем студентам, создаем запись связи задачи и ученика, отправляем оповещение
        if lesson.tasks and student_ids:
            for task in lesson.tasks:
                existing = await session.scalars(
                    select(TaskProgress.user_id).where(
                        TaskProgress.lesson_id == lesson_id,
                        TaskProgress.task_id == task.id,
                        TaskProgress.user_id.in_(student_ids),
                    )
                )
                existing_user_ids = set(existing)

                new_records = [
                    TaskProgress(
                        user_id=sid,
                        task_id=task.id,
                        lesson_id=lesson_id,
                        group_id=group_id,
                        status="pending",
                    )
                    for sid in student_ids
                    if sid not in existing_user_ids
                ]

                session.add_all(new_records)
                
        await session.commit()
        await callback.answer("✅ Урок открыт.", show_alert=True)

        if student_ids:
            msg = (
                f"📢 Учитель открыл новый урок в вашей группе: {group.title}\n\n"
                f"Тема: «{lesson.title}» 📘\n"
                f"Всего заданий: {len(lesson.tasks)}\n\n"
                f"Чтo-бы приступить к выполнению выберите соответствующий пункт в меню(/menu)"
            )

            for uid in student_ids:
                try:
                    await bot.send_message(uid, msg)
                except Exception as e:
                    print(f"⚠️ Не удалось отправить сообщение {uid}: {e}")
