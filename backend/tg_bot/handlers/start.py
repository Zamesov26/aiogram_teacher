from aiogram import Router
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from backend.services.link_service import LinkService
from backend.services.user_service import UserService

router = Router()


@router.message(CommandStart(deep_link=True))
async def start_referral(
    message: Message,
    command: CommandObject,
    session_factory: async_sessionmaker[AsyncSession],
):
    referral_code = command.args
    user_id = message.from_user.id
    async with session_factory() as session:
        await UserService(session).get_or_create_user(message.from_user)
        is_success = await LinkService(session).find_link(user_id, referral_code)
    if not is_success:
        await message.answer(
            "❌ Ссылка недействительна или срок её действия истёк\n"
            "Пожалуйста, проверьте правильность ссылки или обратитесь к отправителю."
        )


@router.message(CommandStart(deep_link=False))
async def start_default(
    message: Message, session_factory: async_sessionmaker[AsyncSession]
):
    async with session_factory() as session:
        _, is_created = await UserService(session).get_or_create_user(message.from_user)
    if is_created:
        await message.answer("Добро пожаловать")
    else:
        await message.answer("Все состояния сброшены")
        # TODO
