from datetime import datetime, date, time
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel

from app.ordering_service.models import OrderStatus


class DatesBase(BaseModel):
    description: str
    start_datetime: datetime
    end_datetime: datetime

    class Config:
        orm_mode = True


class DatesDB(DatesBase):
    id: UUID
    order_id: UUID


class DatesCreate(DatesBase):
    order_id: UUID


class DatesUpdate(DatesBase):
    description: Optional[str]
    start_datetime: Optional[datetime]
    end_datetime: Optional[datetime]


class CommentBase(BaseModel):
    text: str

    class Config:
        orm_mode = True


class CommentDB(CommentBase):
    id: UUID
    author_id: UUID
    order_id: UUID
    created_date: datetime
    updated_date: Optional[datetime]


class CommentCreate(CommentBase):
    author_id: Optional[UUID]
    order_id: Optional[UUID]
    created_date: datetime
    updated_date: datetime


class CommentUpdate(CommentBase):
    updated_date: datetime

class ReferencesBase(BaseModel):
    photo: str
    about: Optional[str]

class ReferencesDB(ReferencesBase):
    id: UUID
    order_id: UUID

    class Config:
        orm_mode = True

class ReferencesCreate(ReferencesBase):
    order_id: UUID

class ReferencesUpdate(ReferencesBase):
    photo: Optional[str]
    about: Optional[str]


class OrderBase(BaseModel):
    status: OrderStatus = OrderStatus.new
    type: str
    subtype: str
    description: Optional[str]
    price: Optional[int]
    barter: Optional[str]
    deadline: Optional[datetime]
    date: Optional[date]
    start_time: Optional[time]
    end_time: Optional[time]
    address: Optional[str]
    models: Optional[str]
    number_of_frames: Optional[int]
    screen_resolution: Optional[str]
    orientation: Optional[str]
    proportions: Optional[str]
    file_format: Optional[str]
    post_processing: Optional[str]
    reason_for_rejection: Optional[str]
    link_for_result: Optional[str]

    class Config:
        orm_mode = True


class OrderDB(OrderBase):
    id: UUID
    customer_id: UUID
    performer_id: UUID
    created_date: datetime
    updated_date: datetime


class OrderCreate(OrderBase):
    customer_id: UUID
    performer_id: UUID
    created_date: datetime
    updated_date: datetime


class OrderUpdate(OrderBase):
    status: Optional[OrderStatus]
    type: Optional[str]
    subtype: Optional[str]


class FullOrderUpdate(OrderUpdate):
    updated_date: datetime


class OrderFullDB(OrderDB):
    dates: List[DatesDB] = []
    comments: List[CommentDB] = []
    references: List[ReferencesDB] = []


class OrderFullCreate(OrderBase):
    dates: List[DatesBase] = []
    comments: List[CommentBase] = []
    references: List[ReferencesBase] = []
