from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .admin_service.routers import router as admin_router
from .auth import get_current_user
from .customer_service.routers import router as customer_router
from .photographer_service.routers import router as photographer_router
from .schemas import BusyDatesBase, BusyDatesCreate, BusyDatesDB, PortfolioPhotoDB, PortfolioCreate, PortfolioPhotoBase, PortfolioPhotoCreate, TagsDB, UserDB, SocialMediaDB, SocialMediaCreate, SocialMediaUpdate, SocialMediaBase, PortfolioDB, PortfolioBase, UserTagsBase, UserTagsCreate, UserTagsDB
from .models_api import BusyDatesAPI, PortfolioAPI, TagsAPI, UserAPI, SocialMediaAPI
from app.db import async_db_session

router = APIRouter()
user_api = UserAPI()
social_media_api = SocialMediaAPI()
portfolio_api = PortfolioAPI()
tags_api = TagsAPI()
busy_dates_api = BusyDatesAPI()

router.include_router(admin_router, prefix="/admins")
router.include_router(customer_router, prefix="/customers")
router.include_router(photographer_router, prefix="/photographers")


@router.get("/me", response_model=UserDB)
async def read_users_me(current_user: UserDB = Depends(get_current_user)) -> UserDB:
    return current_user


@router.get("/{user_id}", response_model=UserDB)
async def user_account(
        user_id: UUID, db: AsyncSession = Depends(async_db_session), current_user: UserDB = Depends(get_current_user)
):
    return await user_api.get_user(db, user_id)


@router.get("/{user_id}/social_medias", response_model=List[SocialMediaDB])
async def user_social_medias(
        user_id: UUID, db: AsyncSession = Depends(async_db_session), current_user: UserDB = Depends(get_current_user)
):
    return await social_media_api.get_social_medias(db, user_id)


@router.post("/{user_id}/social_medias", response_model=List[SocialMediaDB])
async def create_user_social_media(
        user_id: UUID, social_media_items: List[SocialMediaBase],
        db: AsyncSession = Depends(async_db_session),
        current_user: UserDB = Depends(get_current_user)
):
    social_media_items = [
        SocialMediaCreate(**social_media_item.dict(), user_id=user_id) for social_media_item in social_media_items
    ]
    return await social_media_api.create_social_media(db, social_media_items)


@router.patch("/{user_id}/social_medias/{social_media_id}", response_model=SocialMediaDB)
async def update_user_social_media(
        user_id: UUID,
        social_media_id: UUID,
        social_media_item: SocialMediaUpdate,
        db: AsyncSession = Depends(async_db_session),
        current_user: UserDB = Depends(get_current_user)
):
    return await social_media_api.update_social_media(db, user_id, social_media_id, social_media_item)


@router.delete("/{user_id}/social_medias/{social_media_id}")
async def delete_user_social_media(
        user_id: UUID,
        social_media_id: UUID,
        db: AsyncSession = Depends(async_db_session),
        current_user: UserDB = Depends(get_current_user)
):
    return await social_media_api.delete_social_media(db, user_id, social_media_id)

@router.post("/{user_id}/portfolios", response_model = PortfolioDB)
async def create_user_portfolio(
        user_id: UUID, portfolio: PortfolioBase, 
        db: AsyncSession = Depends(async_db_session), 
        current_user: UserDB = Depends(get_current_user)
): 
    portfolio = PortfolioCreate(**portfolio.dict(), user_id=user_id)
    return await portfolio_api.create_portfolio(db, portfolio)

@router.get("/{user_id}/portfolios", response_model = List[PortfolioDB])
async def get_user_portfolios(
        user_id: UUID,
        db: AsyncSession = Depends(async_db_session), 
        current_user: UserDB = Depends(get_current_user)
):
    return await portfolio_api.get_portfolios(db, user_id)

@router.delete("/portfolios/{portfolio_id}")
async def delete_portfolio(
        portfolio_id: UUID,
        db: AsyncSession = Depends(async_db_session),
        current_user: UserDB = Depends(get_current_user)
):
    return await portfolio_api.delete_portfolio(db, portfolio_id)

@router.post("/portfolios/photo", response_model = PortfolioPhotoDB)
async def create_user_portfolio_photo(
        portfolio_photo: PortfolioPhotoBase, 
        db: AsyncSession = Depends(async_db_session), 
        current_user: UserDB = Depends(get_current_user)
):
    portfolio_photo = PortfolioPhotoCreate(**portfolio_photo.dict())
    return await portfolio_api.create_portfolio_photo(db, portfolio_photo)

@router.get("/porftfolios/{portfolio_id}/photos", response_model = List[PortfolioPhotoDB])
async def get_portfolio_photos(
        portfolio_id: UUID,
        db: AsyncSession = Depends(async_db_session), 
        current_user: UserDB = Depends(get_current_user)
):
    return await portfolio_api.get_portfolio_photos(db, portfolio_id)

@router.get("/{user_id}/portfolios/photos", response_model = List[PortfolioPhotoDB])
async def get_user_photos(
        user_id: UUID,
        db: AsyncSession = Depends(async_db_session), 
        current_user: UserDB = Depends(get_current_user)
):
    return await portfolio_api.get_user_photos(db, user_id)

@router.delete("portfolios/photos/{photo_id}")
async def delete_portfolio_photo(
        photo_id: UUID,
        db: AsyncSession = Depends(async_db_session), 
        current_user: UserDB = Depends(get_current_user)  
):
    return await portfolio_api.delete_portfolio_photo(db, photo_id)

@router.post("/{user_id}/tags/{tag_id}", response_model = UserTagsDB)
async def create_user_tag(
        user_id: UUID, tag_id: UUID, 
        db: AsyncSession = Depends(async_db_session), 
        current_user: UserDB = Depends(get_current_user)
):
    user_tag_item = UserTagsCreate(tag_id=tag_id, user_id=user_id)

    return await tags_api.create_user_tag(db, user_tag_item)

@router.get("/{user_id}/tags", response_model = List[TagsDB])
async def get_user_tags(
        user_id: UUID, 
        db: AsyncSession = Depends(async_db_session), 
        current_user: UserDB = Depends(get_current_user)
):
    return await tags_api.get_user_tags(db, user_id)

@router.delete("/{user_id}/tags/{tag_id}")
async def delete_user_tag(
        tag_id: UUID, user_id: UUID, 
        db: AsyncSession = Depends(async_db_session),
        current_user: UserDB = Depends(get_current_user)
):
    return await tags_api.delete_user_tag(db, user_id, tag_id)

@router.get("/{user_id}/busy_dates", response_model = List[BusyDatesDB])
async def get_user_busy_dates(
        user_id: UUID,
        db: AsyncSession = Depends(async_db_session),
        current_user: UserDB = Depends(get_current_user)    
):
    return await busy_dates_api.get_busy_dates(db, user_id)

@router.post("/{user_id}/busy_dates", response_model = List[BusyDatesDB])
async def create_busy_date(
        user_id: UUID, busy_dates: List[BusyDatesBase],
        db: AsyncSession = Depends(async_db_session),
        current_user: UserDB = Depends(get_current_user)     
):
    busy_dates = [
        BusyDatesCreate(**busy_date.dict(), user_id = user_id) for busy_date in busy_dates
        ]
    return await busy_dates_api.create_busy_dates(db, busy_dates)

@router.delete("/{user_id}/busy_dates/{busy_date_id}")
async def delete_busy_date(
        user_id: UUID, busy_date_id: UUID,
        db: AsyncSession = Depends(async_db_session),
        current_user: UserDB = Depends(get_current_user) 
):
    return await busy_dates_api.deleate_busy_dates(db, user_id, busy_date_id)
