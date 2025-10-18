from aiogram import Router, F
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database.models import TGAdmin, Teacher, TelegramUser

router = Router()


class StudentAction(CallbackData, prefix="student"):
    action: str
    id: int


@router.callback_query(F.data == "role_teacher")
async def handle_teacher(callback: CallbackQuery, db_session: AsyncSession, bot):
    user = callback.from_user

    await callback.message.answer(
        "📨 Ваша заявка отправлена. Ожидайте подтверждения администратора."
    )
    await callback.answer()

    admins = await db_session.scalars(select(TGAdmin))
    admin_list = admins.all()
    if not admin_list:
        await callback.message.answer("⚠️ Нет администраторов для подтверждения заявки.")
        return

    text = (
        f"👤 <b>Новый запрос на роль Учителя</b>\n\n"
        f"Имя: {user.first_name or ''} {user.last_name or ''}\n"
        f"Username: @{user.username if user.username else '—'}\n"
        f"ID: <code>{user.id}</code>\n\n"
        f"✅ Чтобы подтвердить: /approve {user.id}\n"
        f"🚫 Чтобы отклонить: /reject {user.id}"
    )

    for admin in admin_list:
        try:
            await bot.send_message(chat_id=admin.user_id, text=text, parse_mode="HTML")
        except Exception as e:
            # Если админ заблокировал бота — просто логируем
            print(f"Не удалось отправить сообщение админу {admin.user_id}: {e}")


class StudentForm(StatesGroup):
    waiting_for_teacher_id = State()


@router.callback_query(F.data == "role_student")
async def handle_student(callback: CallbackQuery, state: FSMContext):
    """Пользователь выбрал роль 'Ученик'."""
    await callback.message.answer("🎒 Введите ID наставника (учителя).")
    await callback.answer()

    await state.set_state(StudentForm.waiting_for_teacher_id)


@router.message(StudentForm.waiting_for_teacher_id)
async def process_teacher_id(
    message: Message, state: FSMContext, db_session: AsyncSession, bot
):
    """Обрабатывает ввод ID наставника, проверяет и отправляет запрос учителю."""
    try:
        teacher_id = int(message.text.strip())
    except ValueError:
        await message.answer("⚠️ Введите корректный числовой ID учителя.")
        return

    teacher = await db_session.scalar(
        select(Teacher).where(Teacher.user_id == teacher_id)
    )
    if not teacher:
        await message.answer("❌ Учитель с таким ID не найден. Попробуйте снова.")
        return

    teacher_user = await db_session.scalar(
        select(TelegramUser).where(TelegramUser.id == teacher_id)
    )

    await message.answer(
        f"📨 Запрос отправлен учителю "
        f"{teacher_user.first_name or ''} {teacher_user.last_name or ''} "
        f"(@{teacher_user.username or '—'}). Ожидайте ответа."
    )

    student = message.from_user
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Принять", callback_data=f"approve_student:{student.id}"
                ),
                InlineKeyboardButton(
                    text="❌ Отклонить", callback_data=f"reject_student:{student.id}"
                ),
            ]
        ]
    )

    text = (
        f"👨‍🎓 Новый запрос от ученика:\n\n"
        f"Имя: {student.first_name or ''} {student.last_name or ''}\n"
        f"Username: @{student.username or '—'}\n"
        f"ID: <code>{student.id}</code>\n\n"
        f"Принять этого ученика?"
    )

    try:
        await bot.send_message(
            chat_id=teacher_id, text=text, parse_mode="HTML", reply_markup=keyboard
        )
    except Exception as e:
        await message.answer("⚠️ Не удалось отправить запрос учителю.")
        print(f"Ошибка при отправке учителю {teacher_id}: {e}")

    await state.clear()


@router.callback_query(F.data.startswith == "approve_student:")
async def handle_student(callback: CallbackQuery, state: FSMContext):
    pass
