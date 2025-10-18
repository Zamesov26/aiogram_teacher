from datetime import datetime, UTC
from enum import Enum
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database.models import LinkEvent


class LinkType(str, Enum):
    REFERRAL_TEACHER = "referral_teacher"
    GROUP_INVITE = "group_invite"
    PROMO = "promo"


class LinkService:
    """Обработка универсальных параметризованных ссылок."""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def find_link(self, user_id: int, code: str):
        """Главная точка входа — обработка ссылки."""

        link = await self.db_session.scalar(
            select(LinkEvent).where(
                LinkEvent.code == code,
                LinkEvent.is_active,
                LinkEvent.expires_at >= datetime.now(UTC),
            )
        )
        if not link:
            return False

        match link.type:
            case LinkType.REFERRAL_TEACHER:
                await self._process_referral_teacher(user_id, link)
            case LinkType.GROUP_INVITE:
                await self._process_group_invite(user_id, link)
            case LinkType.PROMO:
                await self._process_group_invite(user_id, link)
            case _:
                print(f"Неизвестный тип ссылки: {link.type}")

        await self.db_session.commit()
        return True

    async def _process_referral_teacher(self, user_id, link):
        # Логика: если пришёл по рефералке
        ...

    async def _process_group_invite(self, user_id, link):
        # Логика: если учитель пригласил на курс
        ...
