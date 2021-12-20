from datetime import datetime
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel

from app.ordering_service.models import OrderStatus


class DatesBase(BaseModel):
    description: str
    order_id: UUID
    start_datetime: datetime
    end_datetime: datetime

    class Config:
        orm_mode = True


class DatesDB(DatesBase):
    id: UUID


class DatesCreate(DatesBase):
    order_id: Optional[UUID]


class DatesUpdate(DatesCreate):
    description: Optional[str]
    start_datetime: Optional[datetime]
    end_datetime: Optional[datetime]


class CommentBase(BaseModel):
    text: str
    author_id: UUID
    order_id: UUID
    created_date: datetime
    updated_date: Optional[datetime]

    class Config:
        orm_mode = True


class CommentDB(CommentBase):
    id: UUID


class CommentCreate(CommentBase):
    author_id: Optional[UUID]
    order_id: Optional[UUID]
    created_date: datetime = datetime.utcnow()
    updated_date: datetime = datetime.utcnow()


class CommentUpdate(CommentCreate):
    text: Optional[str]
    author_id: Optional[UUID]
    order_id: Optional[UUID]
    created_date: Optional[datetime]
    updated_date: datetime = datetime.utcnow()


class OrderBase(BaseModel):
    status: OrderStatus
    title: str
    description: str
    price: int
    customer_id: UUID
    performer_id: UUID
    created_date: datetime
    updated_date: datetime

    class Config:
        orm_mode = True


class OrderDB(OrderBase):
    id: UUID


class OrderCreate(OrderBase):
    status: OrderStatus = OrderStatus.new
    price: Optional[int]
    created_date: datetime = datetime.utcnow()
    updated_date: datetime = datetime.utcnow()
    customer_id: Optional[UUID]
    performer_id: Optional[UUID]


class OrderUpdate(OrderCreate):
    title: Optional[str]
    status: Optional[OrderStatus]
    description: Optional[str]
    created_date: Optional[datetime]
    updated_date: datetime = datetime.utcnow()


class OrderFullDB(OrderDB):
    dates: List[DatesDB] = []
    comments: List[CommentDB] = []


class OrderFullCreate(OrderCreate):
    dates: List[DatesCreate] = []
    comments: List[CommentCreate] = []
