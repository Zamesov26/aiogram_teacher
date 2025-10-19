import secrets
from datetime import datetime, UTC, timedelta
from sqlite3 import IntegrityError

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database.models import LinkEvent, Group
from backend.database.models.group import GroupUser
from backend.database.models.link_event import LinkType
from backend.services.exceptions.link_exceptions import (
    InvalidLinkError,
    GroupNotFoundError,
    AlreadyInGroupError,
    GroupJoinError,
)


# TODO добавить коммент при создании
class LinkService:
    """Обработка универсальных параметризованных ссылок."""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_group_invite_code(
        self,
        creator_id: int,
        group_id: int,
        *,
        expires_in_hours: int | None = 24,
        is_one_time: bool = False,
    ) -> LinkEvent:
        """Создаёт код для приглашения в группу."""

        code = secrets.token_urlsafe(10)

        expires_at = (
            datetime.now(UTC) + timedelta(hours=expires_in_hours)
            if expires_in_hours
            else None
        )

        link = LinkEvent(
            code=code,
            type=LinkType.GROUP_INVITE,
            creator_id=creator_id,
            payload={"group_id": group_id},
            is_active=True,
            is_one_time=is_one_time,
            expires_at=expires_at,
        )

        self.db_session.add(link)
        await self.db_session.commit()
        await self.db_session.refresh(link)

        return link

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
                await self._process_promo(user_id, link)
            case _:
                print(f"Неизвестный тип ссылки: {link.type}")

        await self.db_session.commit()
        return True

    async def _process_group_invite(self, user_id: int, link: LinkEvent):
        """Добавление пользователя в группу по ссылке."""
        group_id = link.payload.get("group_id")
        if not group_id:
            raise InvalidLinkError("Ссылка не содержит информации о группе")

        # Проверяем, что группа существует и активна
        group = await self.db_session.scalar(
            select(Group).where(Group.id == group_id, Group.is_active.is_(True))
        )
        if not group:
            raise GroupNotFoundError("Группа не найдена или неактивна")

        # Проверяем, не состоит ли пользователь уже в группе
        existing = await self.db_session.scalar(
            select(GroupUser).where(
                GroupUser.group_id == group_id,
                GroupUser.user_id == user_id,
            )
        )
        if existing:
            raise AlreadyInGroupError("Пользователь уже в группе")

        # Добавляем нового участника
        member = GroupUser(
            group_id=group_id,
            user_id=user_id,
            role="student",
            link_event_id=link.id,
            joined_at=datetime.now(UTC),
        )
        self.db_session.add(member)

        try:
            await self.db_session.commit()
        except IntegrityError as e:
            await self.db_session.rollback()
            raise GroupJoinError(f"Ошибка при добавлении в группу: {e}")

        # Если ссылка одноразовая
        if link.is_one_time:
            link.is_active = False
            await self.db_session.commit()

        return group

    async def _process_referral_teacher(self, user_id, link):
        # Логика: если пришёл по рефералке
        ...

    async def _process_promo(self, user_id, link):
        # Логика: если учитель пригласил на курс
        ...
