from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import Photographer, PhotographerDB, PhotographerCreate, PhotographerUpdate
from .service import get_photographers, get_photographer, create_photographer, update_photographer
from app.db import async_db_session

router = APIRouter()


@router.get("/", response_model=List[Photographer])
async def photographers(db: AsyncSession = Depends(async_db_session)):
    users = await get_photographers(db)
    return [Photographer(**user.dict()) for user in users]


@router.post("/", response_model=PhotographerDB)
async def create_photographer_account(photographer: PhotographerCreate, db: AsyncSession = Depends(async_db_session)):
    user = await create_photographer(db, photographer)
    return user


@router.get("/{user_id}", response_model=Photographer)
async def photographer_account(user_id: UUID, db: AsyncSession = Depends(async_db_session)):
    user = await get_photographer(db, user_id)
    return Photographer(**dict(user))


@router.patch("/{user_id}", response_model=Photographer)
async def update_photographer_account(user_id: UUID, photographer: PhotographerUpdate, db: AsyncSession = Depends(async_db_session)):
    user = await update_photographer(db, user_id, photographer)
    return Photographer(**user.dict())
