import logging
from typing import List
from uuid import UUID

from sqlalchemy import update, delete, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.user_service.models import Roles, User, SocialMedia
from app.user_service.schemas import UserDB, UserCreate, UserUpdate
from app.user_service.social_media.schemas import SocialMediaDB, SocialMediaCreate, SocialMediaUpdate

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
        query = select(User).where(User.role == self.role).order_by(User.created_date)
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
        query = update(User).where(User.id == user_id).values(**user.dict(exclude_unset=True))
        await db.execute(query)
        await db.commit()
        return await self.get_user(db, user_id)


class SocialMediaAPI:
    model_db = SocialMediaDB
    model_create = SocialMediaCreate
    model_update = SocialMediaUpdate

    async def get_social_medias(self, db: AsyncSession, user_id: UUID) -> List[model_db]:
        query = select(SocialMedia).where(SocialMedia.user_id == user_id)
        social_medias = await db.execute(query)
        social_medias = social_medias.scalars().all()
        return [self.model_db.from_orm(social_media) for social_media in social_medias]

    async def get_social_media(self, db: AsyncSession, user_id: UUID, social_media_id: UUID) -> model_db:
        query = select(SocialMedia).where(and_(SocialMedia.user_id == user_id, SocialMedia.id == social_media_id))
        social_media = await db.execute(query)
        try:
            social_media = social_media.scalars().one()
        except Exception as exc:
            logger.error(f"Social media doesn't exist {exc}")
            raise
        return self.model_db.from_orm(social_media)

    async def create_social_media(self, db: AsyncSession, social_medias: List[model_create]) -> List[model_db]:
        new_social_medias = [SocialMedia(**social_media.dict()) for social_media in social_medias]
        async with db.begin():
            for new_social_media in new_social_medias:
                db.add(new_social_media)
        for new_social_media in new_social_medias:
            await db.refresh(new_social_media)
        return [self.model_db.from_orm(new_social_media) for new_social_media in new_social_medias]

    async def update_social_media(
            self, db: AsyncSession, user_id: UUID, social_media_id: UUID, social_media: model_update
    ) -> model_db:
        query = update(SocialMedia) \
            .where(and_(SocialMedia.user_id == user_id, SocialMedia.id == social_media_id)) \
            .values(**social_media.dict(exclude_unset=True))
        await db.execute(query)
        await db.commit()
        return await self.get_social_media(db, user_id, social_media_id)

    async def delete_social_media(self, db: AsyncSession, user_id: UUID, social_media_id: UUID) -> None:
        query = delete(SocialMedia).where(and_(SocialMedia.user_id == user_id, SocialMedia.id == social_media_id))
        await db.execute(query)
        await db.commit()
