import logging
from datetime import datetime
from typing import List
from uuid import UUID


from sqlalchemy import update, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.ordering_service.models import Order, Dates, Comment
from app.ordering_service.schemas import (
    OrderDB, OrderCreate, OrderUpdate,
    CommentDB, CommentCreate, CommentUpdate,
    DatesDB, DatesCreate, DatesUpdate
)


logger = logging.getLogger(__name__)


class OrderAPI:
    model_db = OrderDB
    model_create = OrderCreate
    model_update = OrderUpdate

    async def get_orders(self, db: AsyncSession, user_id: UUID) -> List[model_db]:
        async with db.begin():
            query = select(Order).\
                where(or_(Order.performer_id == user_id, Order.customer_id == user_id)).\
                order_by(Order.updated_date)
            orders = await db.execute(query)
        orders = orders.scalars().all()
        return [self.model_db.from_orm(order) for order in orders]

    async def get_order(self, db: AsyncSession, order_id: UUID) -> model_db | None:
        async with db.begin():
            query = select(Order).where(Order.id == order_id)
            order = await db.execute(query)
        try:
            order = order.scalar()
        except Exception as exc:
            logger.error(f"Order doesn't exist {exc}")
            raise
        if order:
            return self.model_db.from_orm(order)
        return None

    async def create_order(self, db: AsyncSession, order: model_create) -> model_db:
        new_order = Order(**order.dict())
        db.add(new_order)
        await db.commit()
        await db.refresh(new_order)
        await db.close()
        return self.model_db.from_orm(new_order)

    async def update_order(self, db: AsyncSession, order_id: UUID, order: model_update) -> model_db:
        async with db.begin():
            query = update(Order).where(Order.id == order_id).values(
                **order.dict(exclude_unset=True)
            )
            await db.execute(query)
        return await self.get_order(db, order_id)


class CommentsAPI:
    model_db = CommentDB
    model_create = CommentCreate
    model_update = CommentUpdate

    async def get_comments(self, db: AsyncSession, order_id: UUID) -> List[model_db]:
        async with db.begin():
            query = select(Comment).where(Comment.order_id == order_id).order_by(Comment.created_date)
            comments = await db.execute(query)
        comments = comments.scalars().all()
        return [self.model_db.from_orm(comment) for comment in comments]

    async def get_comment(self, db: AsyncSession, comment_id: UUID) -> model_db | None:
        async with db.begin():
            query = select(Comment).where(Comment.id == comment_id)
            comment = await db.execute(query)
        try:
            comment = comment.scalar()
        except Exception as exc:
            logger.error(f"Comment doesn't exist {exc}")
            raise
        if comment:
            return self.model_db.from_orm(comment)
        return None

    async def create_comment(self, db: AsyncSession, comment: model_create) -> model_db:
        new_comment = Comment(**comment.dict())
        db.add(new_comment)
        await db.commit()
        await db.refresh(new_comment)
        await db.close()
        return self.model_db.from_orm(new_comment)

    async def update_comment(self, db: AsyncSession, comment_id: UUID, comment: model_update) -> model_db:
        async with db.begin():
            query = update(Comment).where(Comment.id == comment_id).values(
                **comment.dict(exclude_unset=True)
            )
            await db.execute(query)
        return await self.get_comment(db, comment_id)


class DatesAPI:
    model_db = DatesDB
    model_create = DatesCreate
    model_update = DatesUpdate

    async def get_dates(self, db: AsyncSession, order_id: UUID) -> List[model_db]:
        async with db.begin():
            query = select(Dates).where(Dates.order_id == order_id).order_by(Dates.start_datetime)
            dates = await db.execute(query)
        dates = dates.scalars().all()
        return [self.model_db.from_orm(date) for date in dates]

    async def get_date(self, db: AsyncSession, date_id: UUID) -> model_db | None:
        async with db.begin():
            query = select(Dates).where(Dates.id == date_id)
            date = await db.execute(query)
        try:
            date = date.scalar()
        except Exception as exc:
            logger.error(f"Date doesn't exist {exc}")
            raise
        if date:
            return self.model_db.from_orm(date)
        return None

    async def create_date(self, db: AsyncSession, date: model_create) -> model_db:
        new_date = Dates(**date.dict())
        db.add(new_date)
        await db.commit()
        await db.refresh(new_date)
        await db.close()
        return self.model_db.from_orm(new_date)

    async def update_date(self, db: AsyncSession, date_id: UUID, date: model_update) -> model_db:
        async with db.begin():
            query = update(Dates).where(Dates.id == date_id).values(**date.dict(exclude_unset=True))
            await db.execute(query)
        return await self.get_date(db, date_id)
