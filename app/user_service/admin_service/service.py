import logging
from typing import List
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import AdminUpdate, AdminCreate, AdminDB
from ..models import Roles
from ..models_api import UserAPI

logger = logging.getLogger(__name__)
admin = UserAPI(Roles.admin, AdminDB, AdminCreate, AdminUpdate)


async def get_admins(db: AsyncSession) -> List[AdminDB]:
    admins: List[AdminDB] = await admin.get_users(db)
    return admins


async def get_admin(db: AsyncSession, user_id: UUID) -> AdminDB:
    gotten_admin: AdminDB = await admin.get_user(db, user_id)
    return gotten_admin


async def create_admin(db: AsyncSession, user: AdminCreate) -> AdminDB:
    created_admin: AdminDB = await admin.create_user(db, user)
    return created_admin


async def update_admin(db: AsyncSession, user_id: UUID, user: AdminUpdate) -> AdminDB:
    updated_admin: AdminDB = await admin.update_user(db, user_id, user)
    return updated_admin
