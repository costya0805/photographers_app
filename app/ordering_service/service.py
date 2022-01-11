from datetime import datetime
from typing import List
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from .models_api import OrderAPI, DatesAPI, CommentsAPI
from .schemas import (
    OrderDB, OrderUpdate,
    OrderFullDB, OrderFullCreate,
    DatesCreate, CommentCreate, CommentDB, CommentUpdate, OrderCreate, FullOrderUpdate, CommentBase
)

order_api = OrderAPI()
date_api = DatesAPI()
comment_api = CommentsAPI()


async def get_user_orders(db: AsyncSession, user_id: UUID) -> List[OrderDB]:
    return await order_api.get_orders(db, user_id)


async def get_user_order(db: AsyncSession, order_id: UUID) -> OrderFullDB:
    order_db = await order_api.get_order(db, order_id)
    dates = await date_api.get_dates(db, order_db.id)
    comments = await comment_api.get_comments(db, order_db.id)
    return OrderFullDB(**order_db.dict(), dates=dates, comments=comments)


async def create_user_order(
        db: AsyncSession, performer_id: UUID, customer_id: UUID, item: OrderFullCreate
) -> OrderFullDB:
    order_item = OrderCreate(
        **item.dict(exclude_unset=True),
        performer_id=performer_id,
        customer_id=customer_id,
        created_date=datetime.utcnow(),
        updated_date=datetime.utcnow()
    )
    order_db = await order_api.create_order(db, order_item)
    dates = []
    comments = []
    for date_item in item.dates:
        dates.append(
            await date_api.create_date(db, DatesCreate(
                **date_item.dict(exclude_unset=True),
                order_id=order_db.id
            )))
    for comment_item in item.comments:
        comments.append(
            await comment_api.create_comment(
                db, CommentCreate(
                    **comment_item.dict(exclude_unset=True),
                    author_id=customer_id,
                    order_id=order_db.id,
                    created_date=datetime.utcnow(),
                    updated_date=datetime.utcnow()
                )
            )
        )
    return OrderFullDB(**order_db.dict(), dates=dates, comments=comments)


async def update_user_order(db: AsyncSession, order_id: UUID, item: OrderUpdate) -> OrderDB:
    order_item = FullOrderUpdate(
        **item.dict(exclude_unset=True),
        updated_date=datetime.utcnow()
    )
    return await order_api.update_order(db, order_id, order_item)


async def create_order_comment(db: AsyncSession, author_id: UUID, order_id: UUID, item: CommentBase) -> CommentDB:
    comment_item = CommentCreate(
        **item.dict(exclude_unset=True),
        author_id=author_id,
        order_id=order_id,
        created_date=datetime.utcnow(),
        updated_date=datetime.utcnow()
    )
    return await comment_api.create_comment(db, comment_item)


async def update_order_comment(db: AsyncSession, comment_id: UUID, item: CommentBase) -> CommentDB:
    comment_item = CommentUpdate(
        **item.dict(exclude_unset=True),
        updated_date=datetime.utcnow()
    )
    return await comment_api.update_comment(db, comment_id, comment_item)
