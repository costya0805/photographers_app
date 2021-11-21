from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .photographer_service.service import get_photographer
from ..db import async_db_session

router = APIRouter()


@router.get("/users/{user_id}")
async def user_account(user_id: UUID, db: AsyncSession = Depends(async_db_session)):
    user = await get_photographer(db, user_id)
    return user
