import logging
from typing import List
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import PhotographerDB, PhotographerCreate, PhotographerUpdate, FullPhotographerCreate, PhotographerFullDB
from ..models import Roles
from ..models_api import BusyDatesAPI, PortfolioAPI, UserAPI, SocialMediaAPI, TagsAPI, PriceListAPI, FeedbackAPI
from ..schemas import (
    BusyDatesDB, PortfolioDB, PortfolioPhotoDB, SocialMediaDB, SocialMediaCreate, TagsDB, TagsCreate, PriceListDB, PriceListCreate, FeedbackDB
)

logger = logging.getLogger(__name__)
photographer_api = UserAPI(Roles.photographer, PhotographerDB, PhotographerCreate, PhotographerUpdate)
social_media_api = SocialMediaAPI()
tags_api = TagsAPI()
price_list_api = PriceListAPI()
feedback_api = FeedbackAPI()
portfolio_api = PortfolioAPI()
busy_dates_api = BusyDatesAPI()


async def get_photographers(db: AsyncSession) -> List[PhotographerDB]:
    photographers: List[PhotographerDB] = await photographer_api.get_users(db)
    return photographers


async def get_photographer(db: AsyncSession, user_id: UUID) -> PhotographerFullDB:
    gotten_photographer: PhotographerDB = await photographer_api.get_user(db, user_id)
    tags: List[TagsDB] = await tags_api.get_user_tags(db, user_id)
    price_list: List[PriceListDB] = await price_list_api.get_price_list(db, user_id)
    feedbacks: List[FeedbackDB] = await feedback_api.get_feedbacks(db, user_id)
    social_medias: List[SocialMediaDB] = await social_media_api.get_social_medias(db, user_id)
    portfolios: List[PortfolioDB] = await portfolio_api.get_portfolios(db, user_id)
    photos: List[PortfolioPhotoDB] = await portfolio_api.get_user_photos(db, user_id)
    busy_dates: List[BusyDatesDB] = await busy_dates_api.get_busy_dates(db, user_id)
    return PhotographerFullDB(**gotten_photographer.dict(), tags=tags, price_list=price_list, feedbacks=feedbacks, social_medias=social_medias, portfolios=portfolios, photos=photos, busy_dates=busy_dates)


async def create_photographer(db: AsyncSession, user: FullPhotographerCreate) -> PhotographerDB:
    photographer = PhotographerCreate(**user.dict(exclude_unset=True))
    created_photographer: PhotographerDB = await photographer_api.create_user(db, photographer)
    await db.close()
    if user.social_medias:
        social_medias: List[SocialMediaDB] = await social_media_api.create_social_media(
            db,
            [SocialMediaCreate(**sm.dict(exclude_unset=True), user_id=created_photographer.id)
             for sm in user.social_medias])
    await db.close()
    if user.tags:
        tags: List[TagsDB] = await tags_api.create_user_tags(
            db, user_id=created_photographer.id, tags=[TagsCreate(**tag.dict(exclude_unset=True)) for tag in user.tags]
        )
    await db.close()
    if user.price_list:
        price_list: List[PriceListDB] = await price_list_api.create_price_list(
            db, [PriceListCreate(**pl.dict(exclude_unset=True), user_id=created_photographer.id) for pl in user.price_list]
        )
    await db.close()
    return created_photographer


async def update_photographer(db: AsyncSession, user_id: UUID, user: PhotographerUpdate) -> PhotographerDB:
    updated_photographer: PhotographerDB = await photographer_api.update_user(db, user_id, user)
    return updated_photographer
