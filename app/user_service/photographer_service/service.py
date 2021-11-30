import logging
from typing import List
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import PhotographerDB, PhotographerCreate, PhotographerUpdate
from ..models import Roles
from ..models_api import UserAPI

logger = logging.getLogger(__name__)
photographer = UserAPI(Roles.photographer, PhotographerDB, PhotographerCreate, PhotographerUpdate)


async def get_photographers(db: AsyncSession) -> List[PhotographerDB]:
    photographers: List[PhotographerDB] = await photographer.get_users(db)
    return photographers


async def get_photographer(db: AsyncSession, user_id: UUID) -> PhotographerDB:
    gotten_photographer: PhotographerDB = await photographer.get_user(db, user_id)
    return gotten_photographer


async def create_photographer(db: AsyncSession, user: PhotographerCreate) -> PhotographerDB:
    created_photographer: PhotographerDB = await photographer.create_user(db, user)
    return created_photographer


async def update_photographer(db: AsyncSession, user_id: UUID, user: PhotographerUpdate) -> PhotographerDB:
    updated_photographer: PhotographerDB = await photographer.update_user(db, user_id, user)
    return updated_photographer
