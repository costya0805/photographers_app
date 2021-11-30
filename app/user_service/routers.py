from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .admin_service.routers import router as admin_router
from .customer_service.routers import router as customer_router
from .photographer_service.routers import router as photographer_router
from .schemas import UserDB
from .models_api import UserAPI, SocialMediaAPI
from .social_media.schemas import SocialMediaDB, SocialMediaCreate, SocialMediaUpdate, SocialMediaBase
from ..db import async_db_session

router = APIRouter()
user = UserAPI()
social_media = SocialMediaAPI()


router.include_router(admin_router, prefix="/admins")
router.include_router(customer_router, prefix="/customers")
router.include_router(photographer_router, prefix="/photographers")


@router.get("/me", response_model=UserDB)
async def self_account(user_id: UUID, db: AsyncSession = Depends(async_db_session)):
    return await user.get_user(db, user_id)


@router.get("/{user_id}", response_model=UserDB)
async def user_account(user_id: UUID, db: AsyncSession = Depends(async_db_session)):
    return await user.get_user(db, user_id)


@router.get("/{user_id}/social_medias", response_model=List[SocialMediaDB])
async def user_social_medias(user_id: UUID, db: AsyncSession = Depends(async_db_session)):
    return await social_media.get_social_medias(db, user_id)


@router.post("/{user_id}/social_medias", response_model=List[SocialMediaDB])
async def create_user_social_medias(
        user_id: UUID, social_media_items: List[SocialMediaBase], db: AsyncSession = Depends(async_db_session)
):
    social_media_items = [
        SocialMediaCreate(**social_media_item.dict(), user_id=user_id) for social_media_item in social_media_items
    ]
    return await social_media.create_social_media(db, social_media_items)


@router.patch("/{user_id}/social_medias/{social_media_id}", response_model=SocialMediaDB)
async def user_social_medias(
        user_id: UUID,
        social_media_id: UUID,
        social_media_item: SocialMediaUpdate,
        db: AsyncSession = Depends(async_db_session)
):
    return await social_media.update_social_media(db, user_id, social_media_id, social_media_item)


@router.delete("/{user_id}/social_medias/{social_media_id}")
async def user_social_medias(
        user_id: UUID,
        social_media_id: UUID,
        db: AsyncSession = Depends(async_db_session)
):
    return await social_media.delete_social_media(db, user_id, social_media_id)
