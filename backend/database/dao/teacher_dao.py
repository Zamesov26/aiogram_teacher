from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database.models import Group


class TeacherDAO:
    """Доступ к данным учителей"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def has_access_to_group(self, teacher_id: int, group_id: int) -> bool:
        """
        Проверяет, принадлежит ли группа конкретному учителю
        и активна ли она.
        """
        query = select(
            exists().where(
                Group.id == group_id,
                Group.teacher_id == teacher_id,
                Group.is_active.is_(True),
            )
        )
        return await self.session.scalar(query)
