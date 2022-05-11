from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .admin_service.routers import router as admin_router
from .auth import get_current_user
from .customer_service.routers import router as customer_router
from .photographer_service.routers import router as photographer_router
from .schemas import PortfolioCreate, UserDB, SocialMediaDB, SocialMediaCreate, SocialMediaUpdate, SocialMediaBase, PortfolioDB, PortfolioBase
from .models_api import PortfolioAPI, UserAPI, SocialMediaAPI
from app.db import async_db_session

router = APIRouter()
user_api = UserAPI()
social_media_api = SocialMediaAPI()
portfolio_api = PortfolioAPI()

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
