from datetime import datetime, UTC

from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy.orm import joinedload

from backend.database.models import Group, TaskProgress, Task, Lesson
from backend.database.models.group import GroupUser, GroupLesson

router = Router()


@router.callback_query(F.data == "get_task")
async def handle_get_task(
    callback: CallbackQuery,
    session_factory: async_sessionmaker[AsyncSession],
):
    user_id = callback.from_user.id

    async with session_factory() as session:
        # Находим активную группу ученика, где есть открытые уроки
        group = await session.scalar(
            select(Group)
            .join(GroupUser, Group.id == GroupUser.group_id)
            .join(GroupLesson, GroupLesson.group_id == Group.id)
            .where(
                GroupUser.user_id == user_id,
                GroupUser.is_active.is_(True),
                GroupLesson.is_open.is_(True),
                Group.is_active.is_(True),
            )
        )

        if not group:
            await callback.message.answer("🚫 У тебя пока нет активных уроков.")
            return

        # Находим первую невыполненную задачу
        tp = await session.scalar(
            select(TaskProgress)
            .join(Task, Task.id == TaskProgress.task_id)
            .where(
                TaskProgress.user_id == user_id,
                TaskProgress.group_id == group.id,
                TaskProgress.status == "pending",
            )
            .options(joinedload(TaskProgress.task))
            .order_by(Task.id.asc())
        )

        if not tp:
            await callback.message.answer("🎉 Все задания уже выполнены!")
            return

        task = tp.task
        lesson = await session.scalar(select(Lesson).where(Lesson.id == tp.lesson_id))

        # Кнопки
        kb = InlineKeyboardBuilder()
        kb.button(text="✅ Выполнил", callback_data=f"task_done:{task.id}")
        kb.button(text="❌ Не получилось", callback_data=f"task_fail:{task.id}")
        kb.adjust(2)

        text = (
            f"📘 <b>{lesson.title}</b>\n\n"
            f"🧩 <b>Задание:</b>\n{task.text}\n\n"
            "Когда закончишь, выбери один из вариантов ниже 👇"
        )
        await callback.message.answer(
            text, reply_markup=kb.as_markup(), parse_mode="HTML"
        )


@router.callback_query(F.data.startswith("task_done:"))
async def handle_task_done(
    callback: CallbackQuery, session_factory: async_sessionmaker[AsyncSession]
):
    task_id = int(callback.data.split(":")[1])
    user_id = callback.from_user.id

    async with session_factory() as session:
        tp = await session.scalar(
            select(TaskProgress).where(
                TaskProgress.user_id == user_id, TaskProgress.task_id == task_id
            )
        )
        if not tp:
            await callback.answer("⚠️ Задание не найдено.", show_alert=True)
            return

        tp.status = "done"
        tp.updated_at = datetime.now(UTC)
        await session.commit()
        await callback.answer(
            "🎉 Отлично! Задание отмечено как выполненное.", show_alert=True
        )
        await callback.message.delete()


@router.callback_query(F.data.startswith("task_fail:"))
async def handle_task_fail(
    callback: CallbackQuery, session_factory: async_sessionmaker[AsyncSession]
):
    task_id = int(callback.data.split(":")[1])
    user_id = callback.from_user.id

    async with session_factory() as session:
        tp = await session.scalar(
            select(TaskProgress).where(
                TaskProgress.user_id == user_id, TaskProgress.task_id == task_id
            )
        )
        if not tp:
            await callback.answer("⚠️ Задание не найдено.", show_alert=True)
            return

        tp.status = "failed"
        tp.updated_at = datetime.now(UTC)
        await session.commit()
        await callback.answer("😞 Не страшно! Попробуешь снова позже.", show_alert=True)
        await callback.message.delete()
