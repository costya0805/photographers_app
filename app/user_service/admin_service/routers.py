from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import AdminUpdate, AdminDB, AdminCreate
from .service import get_admins, get_admin, create_admin, update_admin
from app.db import async_db_session
from ..auth import get_current_user, is_the_same_user
from ..schemas import UserDB

router = APIRouter()


@router.get("/", response_model=List[AdminDB])
async def admins(db: AsyncSession = Depends(async_db_session), current_user: UserDB = Depends(get_current_user)):
    return await get_admins(db)


@router.post("/", response_model=AdminDB)
async def create_admin_account(admin: AdminCreate, db: AsyncSession = Depends(async_db_session)):
    user = await create_admin(db, admin)
    return user


@router.get("/{user_id}", response_model=AdminDB)
async def admin_account(
        user_id: UUID, db: AsyncSession = Depends(async_db_session), current_user: UserDB = Depends(get_current_user)
):
    return await get_admin(db, user_id)


@router.patch("/{user_id}", response_model=AdminDB)
async def update_admin_account(
        user_id: UUID,
        admin: AdminUpdate,
        db: AsyncSession = Depends(async_db_session),
        current_user: UserDB = Depends(get_current_user)
):
    await is_the_same_user(user_id, current_user)
    return await update_admin(db, user_id, admin)
