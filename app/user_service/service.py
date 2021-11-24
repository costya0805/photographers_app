import logging
from typing import List
from uuid import UUID

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.user_service.models import Roles, User
from app.user_service.schemas import UserDB, UserCreate, UserUpdate

logger = logging.getLogger(__name__)


class UserAPI:
    model_db = UserDB
    model_create = UserCreate
    model_update = UserUpdate

    def __init__(self, role=Roles.customer, model_db=UserDB, model_create=UserCreate, model_update=UserUpdate):
        self.role: Roles = role
        self.model_db = model_db
        self.model_create = model_create
        self.model_update = model_update

    async def get_users(self, db: AsyncSession) -> List[model_db]:
        query = select(User).where(User.role == self.role).order_by(User.creation_date)
        users = await db.execute(query)
        users = users.scalars().all()
        return [self.model_db.from_orm(user) for user in users]

    async def get_user(self, db: AsyncSession, user_id: UUID) -> model_db:
        query = select(User).where(User.id == user_id)
        user = await db.execute(query)
        try:
            user = user.scalars().one()
        except Exception as exc:
            logger.error(f"User doesn't exist {exc}")
            raise
        return self.model_db.from_orm(user)

    async def create_user(self, db: AsyncSession, user: model_create) -> model_db:
        new_user = User(**user.dict())
        async with db.begin():
            db.add(new_user)
        await db.refresh(new_user)
        return self.model_db.from_orm(new_user)

    async def update_user(self, db: AsyncSession, user_id: UUID, user: model_update) -> model_db:
        query = update(User).where(User.id == user_id).values(user)
        updated_user = await db.execute(query)
        return updated_user
