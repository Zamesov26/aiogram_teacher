from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.database.models import Lesson
from backend.database.dependencies import get_session

router = APIRouter(prefix="/lessons", tags=["lessons"])


@router.get("/")
async def list_lessons(session: AsyncSession = Depends(get_session)):
    lessons = await session.scalars(select(Lesson))
    return lessons.all()
