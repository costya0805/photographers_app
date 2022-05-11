from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import PhotographerDB, PhotographerUpdate, FullPhotographerCreate, PhotographerFullDB
from .service import get_photographers, get_photographer, create_photographer, update_photographer
from app.db import async_db_session
from ..auth import get_current_user, is_the_same_user
from ..schemas import UserDB

router = APIRouter()


@router.get("/", response_model=List[PhotographerDB])
async def photographers(db: AsyncSession = Depends(async_db_session)):
    return await get_photographers(db)


@router.post("/", response_model=PhotographerDB)
async def create_photographer_account(
        photographer: FullPhotographerCreate,
        db: AsyncSession = Depends(async_db_session)
):
    user = await create_photographer(db, photographer)
    return user


@router.get("/{user_id}", response_model=PhotographerFullDB)
async def photographer_account(
        user_id: UUID, db: AsyncSession = Depends(async_db_session), current_user: UserDB = Depends(get_current_user)
):
    return await get_photographer(db, user_id)


@router.patch("/{user_id}", response_model=PhotographerDB)
async def update_photographer_account(
        user_id: UUID,
        photographer: PhotographerUpdate,
        db: AsyncSession = Depends(async_db_session),
        current_user: UserDB = Depends(get_current_user)
):
    await is_the_same_user(user_id, current_user)
    return await update_photographer(db, user_id, photographer)
