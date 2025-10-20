from datetime import datetime, UTC

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database.models import GroupLesson


class AssignmentsService:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def open_lesson_for_group(
        self, group_id: int, lesson_id: int, teacher_id: int
    ):
        gl = await self.db_session.scalar(
            select(GroupLesson).where(
                GroupLesson.group_id == group_id,
                GroupLesson.lesson_id == lesson_id,
            )
        )
        if not gl:
            gl = GroupLesson(
                group_id=group_id,
                lesson_id=lesson_id,
                is_open=True,
                opened_at=datetime.now(UTC),
                opened_by_id=teacher_id,
            )
            self.db_session.add(gl)
        return gl
