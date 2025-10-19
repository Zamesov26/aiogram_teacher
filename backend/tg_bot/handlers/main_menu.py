from aiogram import Router, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy.orm import raiseload, joinedload, with_loader_criteria

from backend.database.models import Group, TelegramUser, Teacher, TGAdmin

router = Router()


@router.message(F.text == "/menu")
async def main_menu(
    message: types.Message, session_factory: async_sessionmaker[AsyncSession]
):
    """Главное меню, собираем динамически в зависимости от роли и состояния."""
    kb = InlineKeyboardBuilder()

    # Общие пункты
    # kb.button(text="📚 Курсы", callback_data="courses_list")
    # kb.button(text="ℹ️ Информация", callback_data="info_menu")

    async with session_factory() as session:
        db_user = await session.scalar(
            select(TelegramUser)
            .where(TelegramUser.id == message.from_user.id)
            .options(
                joinedload(TelegramUser.group_memberships),
                with_loader_criteria(Group, Group.is_active == True),
                joinedload(TelegramUser.teacher),
                with_loader_criteria(Teacher, Teacher.is_active == True),
                joinedload(TelegramUser.admin),
                with_loader_criteria(TGAdmin, TGAdmin.is_active == True),
                raiseload("*"),
            )
        )

        if db_user.group_memberships:
            kb.button(text="🎓 Получить задание", callback_data="get_task")
            kb.button(text="Настройки курсов", callback_data="group_settings")

        if db_user.teacher:
            kb.button(text="👩‍🏫 Мои группы", callback_data="teacher_groups")
            kb.button(text="⚙️ Настройки учителя", callback_data="teacher_settings")

        if db_user.admin:
            kb.button(text="🛠 Админ-панель", callback_data="admin_panel")

    kb.adjust(2)
    await message.answer("Главное меню 🏠", reply_markup=kb.as_markup())
