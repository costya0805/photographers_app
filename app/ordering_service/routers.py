from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import async_db_session
from app.ordering_service.schemas import OrderDB, OrderUpdate, OrderFullCreate, OrderFullDB, CommentCreate, \
    CommentUpdate, CommentDB
from app.ordering_service.service import get_user_orders, get_user_order, create_user_order, update_user_order, \
    create_order_comment, update_order_comment

router = APIRouter()


@router.get("/{user_id}/orders", response_model=List[OrderDB])
async def get_orders(user_id: UUID, db: AsyncSession = Depends(async_db_session)) -> List[OrderDB]:
    return await get_user_orders(db, user_id)


@router.get("/{user_id}/orders/{order_id}", response_model=OrderFullDB)
async def get_order(user_id: UUID, order_id: UUID, db: AsyncSession = Depends(async_db_session)) -> OrderFullDB:
    return await get_user_order(db, user_id, order_id)


@router.post("/{user_id}/orders", response_model=OrderFullDB)
async def create_order(
        user_id: UUID, order_item: OrderFullCreate, db: AsyncSession = Depends(async_db_session)
) -> OrderFullDB:
    return await create_user_order(db, user_id, order_item)


@router.patch("/{user_id}/orders/{order_id}", response_model=OrderDB)
async def update_order(
        user_id: UUID, order_id: UUID, order_item: OrderUpdate, db: AsyncSession = Depends(async_db_session)
) -> OrderDB:
    return await update_user_order(db, order_id, order_item)


@router.post("/{user_id}/orders/{order_id}/comments/", response_model=CommentDB)
async def create_comment(
        user_id: UUID, order_id: UUID, comment_item: CommentCreate, db: AsyncSession = Depends(async_db_session)
) -> CommentDB:
    return await create_order_comment(db, user_id, order_id, comment_item)


@router.patch("/{user_id}/orders/{order_id}/comments/{comment_id}", response_model=CommentDB)
async def update_comment(
        user_id: UUID,
        order_id: UUID,
        comment_id: UUID,
        comment_item: CommentUpdate,
        db: AsyncSession = Depends(async_db_session)
) -> CommentDB:
    return await update_order_comment(db, comment_id, comment_item)
