from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import PhotographerDB, PhotographerCreate, PhotographerUpdate
from .service import get_photographers, get_photographer, create_photographer, update_photographer
from app.db import async_db_session

router = APIRouter()


@router.get("/", response_model=List[PhotographerDB])
async def photographers(db: AsyncSession = Depends(async_db_session)):
    return await get_photographers(db)


@router.post("/", response_model=PhotographerDB)
async def create_photographer_account(photographer: PhotographerCreate, db: AsyncSession = Depends(async_db_session)):
    user = await create_photographer(db, photographer)
    return user


@router.get("/{user_id}", response_model=PhotographerDB)
async def photographer_account(user_id: UUID, db: AsyncSession = Depends(async_db_session)):
    return await get_photographer(db, user_id)


@router.patch("/{user_id}", response_model=PhotographerDB)
async def update_photographer_account(
        user_id: UUID, photographer: PhotographerUpdate, db: AsyncSession = Depends(async_db_session)
):
    return await update_photographer(db, user_id, photographer)
