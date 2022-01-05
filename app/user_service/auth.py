from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import async_db_session
from app.ordering_service.models_api import OrderAPI
from app.ordering_service.schemas import OrderDB
from app.user_service.models import Roles
from app.user_service.models_api import UserAPI
from app.user_service.schemas import UserDB


user_api = UserAPI()
order_api = OrderAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def fake_decode_token(db: AsyncSession, token: str) -> UserDB:
    return await user_api.get_user_by_email(db, token)


async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(async_db_session)) -> UserDB:
    current_user: UserDB = await fake_decode_token(db, token)
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return current_user


async def get_customer(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(async_db_session)) -> UserDB:
    current_user: UserDB = await fake_decode_token(db, token)
    if not current_user or not current_user.role == Roles.customer:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return current_user


async def get_photographer(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(async_db_session)) -> UserDB:
    current_user: UserDB = await fake_decode_token(db, token)
    if not current_user or not current_user.role == Roles.photographer:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return current_user


async def is_the_same_user(user_id: UUID, current_user: UserDB) -> None:
    if current_user.role != Roles.admin and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def is_order_performer(order_performer: UUID, current_user: UserDB) -> bool:
    if current_user.role == Roles.photographer and order_performer == current_user.id:
        return True
    return False


async def is_order_customer(order_customer: UUID, current_user: UserDB) -> bool:
    if current_user.role == Roles.customer and order_customer == current_user.id:
        return True
    return False


async def is_performer_or_customer(current_user: UserDB, order: OrderDB) -> None:
    if current_user.role != Roles.admin \
            and not await is_order_performer(order.performer_id, current_user) \
            and not await is_order_customer(order.customer_id, current_user):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
