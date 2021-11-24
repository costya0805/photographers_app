from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import Admin, AdminUpdate, AdminDB, AdminCreate
from .service import get_admins, get_admin, create_admin, update_admin
from app.db import async_db_session

router = APIRouter()


@router.get("/", response_model=List[Admin])
async def admins(db: AsyncSession = Depends(async_db_session)):
    users = await get_admins(db)
    return [Admin(**user.dict()) for user in users]


@router.post("/", response_model=AdminDB)
async def create_admin_account(admin: AdminCreate, db: AsyncSession = Depends(async_db_session)):
    user = await create_admin(db, admin)
    return user


@router.get("/{user_id}", response_model=Admin)
async def admin_account(user_id: UUID, db: AsyncSession = Depends(async_db_session)):
    user = await get_admin(db, user_id)
    return user


@router.patch("/{user_id}", response_model=Admin)
async def update_admin_account(user_id: UUID, admin: AdminUpdate, db: AsyncSession = Depends(async_db_session)):
    user = await update_admin(db, user_id, admin)
    return Admin(**user.dict())
