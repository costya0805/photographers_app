from typing import List
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import PhotographerUpdate, PhotographerCreate, PhotographerDB


async def get_photographers(db: AsyncSession) -> List[PhotographerDB]:
    pass


async def get_photographer(db: AsyncSession, user_id: UUID) -> PhotographerDB:
    pass


async def create_photographer(db: AsyncSession, user: PhotographerCreate) -> PhotographerDB:
    pass


async def update_photographer(db: AsyncSession, user_id: UUID, photographer: PhotographerUpdate) -> PhotographerDB:
    pass
