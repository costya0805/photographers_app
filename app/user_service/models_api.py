import logging
from typing import List
from uuid import UUID

from sqlalchemy import update, delete, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.user_service.models import PortfolioPhoto, Roles, User, SocialMedia, Tags, UserTags, PriceList, Feedbacks, Portfolio
from app.user_service.schemas import (
    PortfolioPhotoDB, PortfolioPhotoCreate, UserDB, UserCreate, UserTagsCreate, UserTagsDB, UserUpdate, SocialMediaDB, SocialMediaCreate, SocialMediaUpdate, PriceListDB, PriceListCreate, FeedbackDB,
    FeedbackCreate, TagsDB, TagsCreate, PortfolioDB, PortfolioCreate, PortfolioUpdate
)

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
        async with db.begin():
            query = select(User).where(User.role == self.role).order_by(User.created_date)
            users = await db.execute(query)
        users = users.scalars().all()
        return [self.model_db.from_orm(user) for user in users]

    async def get_user(self, db: AsyncSession, user_id: UUID) -> model_db:
        async with db.begin():
            query = select(User).where(User.id == user_id)
            user = await db.execute(query)
        try:
            user = user.scalar()
        except Exception as exc:
            logger.error(f"User doesn't exist {exc}")
            raise
        return self.model_db.from_orm(user)

    async def get_user_by_email(self, db: AsyncSession, email: str) -> model_db | None:
        async with db.begin():
            query = select(User).where(User.email == email)
            user = await db.execute(query)
        try:
            user = user.scalar()
        except Exception as exc:
            logger.error(f"User doesn't exist {exc}")
            return None
        return self.model_db.from_orm(user)

    async def create_user(self, db: AsyncSession, user: model_create) -> model_db:
        new_user = User(**user.dict())
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        await db.close()
        new_user = self.model_db.from_orm(new_user)
        return new_user

    async def update_user(self, db: AsyncSession, user_id: UUID, user: model_update) -> model_db:
        async with db.begin():
            query = update(User).where(User.id == user_id).values(**user.dict(exclude_unset=True))
            await db.execute(query)
        return await self.get_user(db, user_id)


class SocialMediaAPI:
    model_db = SocialMediaDB
    model_create = SocialMediaCreate
    model_update = SocialMediaUpdate

    async def get_social_medias(self, db: AsyncSession, user_id: UUID) -> List[model_db]:
        async with db.begin():
            query = select(SocialMedia).where(SocialMedia.user_id == user_id)
            social_medias = await db.execute(query)
        social_medias = social_medias.scalars().all()
        return [self.model_db.from_orm(social_media) for social_media in social_medias]

    async def get_social_media(self, db: AsyncSession, user_id: UUID, social_media_id: UUID) -> model_db:
        async with db.begin():
            query = select(SocialMedia).where(and_(SocialMedia.user_id == user_id, SocialMedia.id == social_media_id))
            social_media = await db.execute(query)
        try:
            social_media = social_media.scalar()
        except Exception as exc:
            logger.error(f"Social media doesn't exist {exc}")
            raise
        return self.model_db.from_orm(social_media)

    async def create_social_media(self, db: AsyncSession, social_medias: List[model_create]) -> List[model_db]:
        new_social_medias = [SocialMedia(**social_media.dict()) for social_media in social_medias]
        for new_social_media in new_social_medias:
            db.add(new_social_media)
        await db.commit()
        for new_social_media in new_social_medias:
            await db.refresh(new_social_media)
        await db.close()
        return [self.model_db.from_orm(new_social_media) for new_social_media in new_social_medias]

    async def update_social_media(
            self, db: AsyncSession, user_id: UUID, social_media_id: UUID, social_media: model_update
    ) -> model_db:
        async with db.begin():
            query = update(SocialMedia) \
                .where(and_(SocialMedia.user_id == user_id, SocialMedia.id == social_media_id)) \
                .values(**social_media.dict(exclude_unset=True))
            await db.execute(query)
        return await self.get_social_media(db, user_id, social_media_id)

    async def delete_social_media(self, db: AsyncSession, user_id: UUID, social_media_id: UUID) -> None:
        async with db.begin():
            query = delete(SocialMedia).where(and_(SocialMedia.user_id == user_id, SocialMedia.id == social_media_id))
            await db.execute(query)


class TagsAPI:
    model_db = TagsDB
    model_create = TagsCreate

    user_model_db = UserTagsDB
    user_model_create = UserTagsCreate

    async def get_tags(self, db: AsyncSession) -> List[model_db]:
        async with db.begin():
            query = select(Tags)
            tags = await db.execute(query)
        tags = tags.scalars().all()
        return [self.model_db.from_orm(tag) for tag in tags]

    async def get_tag(self, db: AsyncSession, tag_id: UUID) -> model_db:
        async with db.begin():
            query = select(Tags).where(Tags.id == tag_id)
            tag = await db.execute(query)
        try:
            tag = tag.scalar()
        except Exception as exc:
            logger.error(f"Tag doesn't exist {exc}")
            raise
        return self.model_db.from_orm(tag)

    async def get_tag_by_name(self, db: AsyncSession, name: str) -> model_db:
        async with db.begin():
            query = select(Tags).where(Tags.name == name)
            tag = await db.execute(query)
        try:
            tag = tag.scalar()
        except Exception as exc:
            logger.error(f"Tag doesn't exist {exc}")
            raise
        return self.model_db.from_orm(tag)

    async def create_tags(self, db: AsyncSession, tags: List[model_create]) -> List[model_db]:
        new_tags = [Tags(**tag.dict()) for tag in tags]
        for new_tag in new_tags:
            db.add(new_tag)
        await db.commit()
        for new_tag in new_tags:
            await db.refresh(new_tag)
        await db.close()
        return [self.model_db.from_orm(new_tag) for new_tag in new_tags]
    
    async def delete_tag(self, db: AsyncSession, tag_id: UUID) -> None:
        async with db.begin():
            query = delete(Tags).where(Tags.id == tag_id)
            await db.execute(query)

    async def get_user_tags(self, db: AsyncSession, user_id: UUID) -> List[model_db]:
        async with db.begin():
            query = select(UserTags).where(UserTags.user_id == user_id)
            user_tags = await db.execute(query)
        try:
            user_tags = user_tags.scalars().all()
        except Exception as exc:
            logger.error(f"User tags doesn't exist {exc}")
            raise
        logger.error(f"Gotten tags: {user_tags}")
        res_tags = []
        for user_tag in user_tags:
            async with db.begin():
                query = select(Tags).where(Tags.id == user_tag.tag_id)
                tag = await db.execute(query)
            try:
                tag = tag.scalar()
                if tag:
                    res_tags.append(tag)
            except Exception as exc:
                logger.error(f"Tags doesn't exist {exc}")
                raise
        logger.error(f"Res tags: {res_tags}")
        return [self.model_db.from_orm(user_tag) for user_tag in res_tags]

    async def create_user_tags(self, db: AsyncSession, user_id: UUID, tags: List[model_create]) -> List[model_db]:
        existed_tags = {tag.name for tag in await self.get_tags(db)}
        tag_names = {tag.name for tag in tags}
        new_tags = tag_names - existed_tags
        new_tags = [Tags(name=tag_name) for tag_name in new_tags]
        if new_tags:
            for tag in new_tags:
                db.add(tag)
            await db.commit()

        res_tags = []
        for tag in tags:
            tag = await self.get_tag_by_name(db, tag.name)
            res_tags.append(self.model_db.from_orm(tag))
            db.add(UserTags(user_id=user_id, tag_id=tag.id))
        await db.commit()
        await db.close()
        return res_tags
    
    async def create_user_tag(self, db: AsyncSession, user_tag: user_model_create) -> user_model_db:
        new_user_tag = UserTags(**user_tag.dict())
        db.add(new_user_tag)
        await db.commit()
        await db.refresh(new_user_tag)
        await db.close()
        new_user_tag = self.user_model_db.from_orm(new_user_tag)
        return new_user_tag

    async def delete_user_tag(self, db: AsyncSession, user_id: UUID, tag_id: UUID) -> None:
        async with db.begin():
            query = delete(UserTags).where(and_(UserTags.user_id == user_id, UserTags.tag_id == tag_id))
            await db.execute(query)


class PriceListAPI:
    model_db = PriceListDB
    model_create = PriceListCreate

    async def get_price_list(self, db: AsyncSession, user_id: UUID) -> List[model_db]:
        async with db.begin():
            query = select(PriceList).where(PriceList.user_id == user_id)
            price_list = await db.execute(query)
        price_list = price_list.scalars().all()
        return [self.model_db.from_orm(price) for price in price_list]

    async def create_price_list(self, db: AsyncSession, price_list: List[model_create]) -> List[model_db]:
        new_price_list = [PriceList(**price.dict()) for price in price_list]
        for price in new_price_list:
            db.add(price)
        await db.commit()
        for price in new_price_list:
            await db.refresh(price)
        await db.close()
        return [self.model_db.from_orm(price) for price in new_price_list]


class FeedbackAPI:
    model_db = FeedbackDB
    model_create = FeedbackCreate

    async def get_feedbacks(self, db: AsyncSession, user_id: UUID) -> List[model_db]:
        async with db.begin():
            query = select(Feedbacks).where(Feedbacks.photographer_id == user_id)
            feedbacks = await db.execute(query)
        feedbacks = feedbacks.scalars().all()
        return [self.model_db.from_orm(feedback) for feedback in feedbacks]

    async def create_feedbacks(self, db: AsyncSession, feedbacks: List[model_create]) -> List[model_db]:
        new_feedbacks = [Feedbacks(**feedback.dict()) for feedback in feedbacks]
        for feedback in new_feedbacks:
            db.add(feedback)
        await db.commit()
        for feedback in new_feedbacks:
            await db.refresh(feedback)
        await db.close()
        return [self.model_db.from_orm(feedback) for feedback in new_feedbacks]

class PortfolioAPI:
    model_db = PortfolioDB
    model_create = PortfolioCreate
    model_update = PortfolioUpdate

    photo_model_db = PortfolioPhotoDB
    photo_model_create = PortfolioPhotoCreate
    

    async def create_portfolio(self, db: AsyncSession, portfolio: model_create) -> model_db:
        new_portfolio = Portfolio(**portfolio.dict())
        db.add(new_portfolio)
        await db.commit()
        await db.refresh(new_portfolio)
        await db.close()
        new_portfolio = self.model_db.from_orm(new_portfolio)
        return new_portfolio

    async def update_portfolio(self, db: AsyncSession, portfolio_id: UUID, portfolio: model_update) -> model_db:
        async with db.begin():
            query = update(Portfolio).where(Portfolio.id == portfolio_id).values(**portfolio.dict(exclude_unset = True))
            await db.execute(query)
        return await self.get_portfolio(db, portfolio_id)
    
    async def get_portfolio(self, db: AsyncSession, portfolio_id: UUID) -> model_db:
        async with db.begin():
            query = select(Portfolio).where(Portfolio.id == portfolio_id)
            portfolio = await db.execute(query)
        try:
            portfolio = portfolio.scalar()
        except Exception as exc:
            logger.error(f"Portfolio dosn't exist {exc}")
            raise
        return self.model_db.from_orm(portfolio)
        
    async def get_portfolios(self, db: AsyncSession, user_id: UUID) -> List[model_db]:
        async with db.begin():
            query = select(Portfolio).where(Portfolio.user_id == user_id)
            portfolios = await db.execute(query)
        portfolios = portfolios.scalars().all()
        return [self.model_db.from_orm(portfolio) for portfolio in portfolios]

    async def delete_portfolio(self, db: AsyncSession, portfolio_id: UUID) -> None:
        async with db.begin():
            query = delete(PortfolioPhoto).where(PortfolioPhoto.portfolio_id == portfolio_id)
            await db.execute(query)
            query = delete(Portfolio).where(Portfolio.id == portfolio_id)
            await db.execute(query)

    async def create_portfolio_photo(self, db: AsyncSession, portfolio_photo: photo_model_create) -> photo_model_db:
        new_portfolio_photo = PortfolioPhoto(**portfolio_photo.dict())
        db.add(new_portfolio_photo)
        await db.commit()
        await db.refresh(new_portfolio_photo)
        await db.close()
        new_portfolio_photo = self.photo_model_db.from_orm(new_portfolio_photo)
        return new_portfolio_photo
        
    async def get_portfolio_photos(self, db: AsyncSession, portfolio_id: UUID) -> List[photo_model_db]:
        async with db.begin():
            query = select(PortfolioPhoto).where(PortfolioPhoto.portfolio_id == portfolio_id)
            portfolio_photos = await db.execute(query)
        portfolio_photos = portfolio_photos.scalars().all()
        return [self.photo_model_db.from_orm(portfolio_photo) for portfolio_photo in portfolio_photos]

    async def delete_portfolio_photo(self, db: AsyncSession, photo_id: UUID) -> None:
        async with db.begin():
            query = delete(PortfolioPhoto).where(PortfolioPhoto.id == photo_id)
            await db.execute(query)

    async def get_user_photos(self, db: AsyncSession, user_id: UUID) -> List[photo_model_db]:
        async with db.begin():
            query = select(Portfolio).where(Portfolio.user_id == user_id)
            portfolios = await db.execute(query)
        portfolios = portfolios.scalars().all()
        res_photos = []
        for portfolio in portfolios:
            async with db.begin():
                query = select(PortfolioPhoto).where(PortfolioPhoto.portfolio_id == portfolio.id)
                photos = await db.execute(query)
            photos = photos.scalars().all()
            if photos:
                for photo in photos:
                    res_photos.append(photo)
        return [self.photo_model_db.from_orm(user_photo) for user_photo in res_photos[:10]]
