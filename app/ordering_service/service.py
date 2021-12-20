from datetime import datetime
from typing import List
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from .models_api import OrderAPI, DatesAPI, CommentsAPI
from .schemas import (
    OrderDB, OrderCreate, OrderUpdate,
    OrderFullDB, OrderFullCreate,
    DatesCreate, CommentCreate, CommentDB, CommentUpdate
)

order = OrderAPI()
date = DatesAPI()
comment = CommentsAPI()


async def get_user_orders(db: AsyncSession, user_id: UUID) -> List[OrderDB]:
    return await order.get_orders(db, user_id)


async def get_user_order(db: AsyncSession, user_id: UUID, order_id: UUID) -> OrderFullDB:
    order_db = await order.get_order(db, order_id)
    dates = await date.get_dates(db, order_db.id)
    comments = await comment.get_comments(db, order_db.id)
    return OrderFullDB(**order_db.dict(), dates=dates, comments=comments)


async def create_user_order(db: AsyncSession, user_id: UUID, item: OrderFullCreate) -> OrderFullDB:
    order_item = OrderCreate(**item.dict(exclude_unset=True), updated_date=datetime.utcnow(), performer_id=user_id)
    order_db = await order.create_order(db, order_item)
    dates = []
    comments = []
    for date_item in item.dates:
        dates.append(await date.create_date(db, DatesCreate(**date_item.dict(exclude_unset=True), order_id=order_db.id)))
    for comment_item in item.comments:
        comments.append(
            await comment.create_comment(
                db, CommentCreate(**comment_item.dict(exclude_unset=True), author_id=user_id, order_id=order_db.id)
            )
        )
    return OrderFullDB(**order_db.dict(), dates=dates, comments=comments)


async def update_user_order(db: AsyncSession, order_id: UUID, order_item: OrderUpdate) -> OrderDB:
    return await order.update_order(db, order_id, order_item)


async def create_order_comment(db: AsyncSession, user_id: UUID, order_id: UUID, item: CommentCreate) -> CommentDB:
    comment_item = CommentCreate(**item.dict(exclude_unset=True), author_id=user_id, order_id=order_id)
    return await comment.create_comment(db, comment_item)


async def update_order_comment(db: AsyncSession, comment_id: UUID, comment_item: CommentUpdate) -> CommentDB:
    return await comment.update_comment(db, comment_id, comment_item)

