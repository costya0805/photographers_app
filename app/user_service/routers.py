from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .admin_service.routers import router as admin_router
from .customer_service.routers import router as customer_router
from .photographer_service.routers import router as photographer_router
from .schemas import UserDB
from .service import UserAPI
from ..db import async_db_session

router = APIRouter()
user = UserAPI()

router.include_router(admin_router, prefix="/admins")
router.include_router(customer_router, prefix="/customers")
router.include_router(photographer_router, prefix="/photographers")


@router.get("/me", response_model=UserDB)
async def self_account(user_id: UUID, db: AsyncSession = Depends(async_db_session)):
    return await user.get_user(db, user_id)


@router.get("/{user_id}", response_model=UserDB)
async def user_account(user_id: UUID, db: AsyncSession = Depends(async_db_session)):
    return await user.get_user(db, user_id)
