from typing import List
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import AdminUpdate, AdminCreate, AdminDB


async def get_admins(db: AsyncSession) -> List[AdminDB]:
    pass


async def get_admin(db: AsyncSession, user_id: UUID) -> AdminDB:
    pass


async def create_admin(db: AsyncSession, user: AdminCreate) -> AdminDB:
    pass


async def update_admin(db: AsyncSession, user_id: UUID, admin: AdminUpdate) -> AdminDB:
    pass
