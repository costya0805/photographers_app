from datetime import datetime
import random
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, validator

from app.user_service.models import Roles, SocialMediaType


def generate_pwd() -> str:
    symbols_list = "+-/*!&$#?=@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    password = ""
    length = random.randint(6, 10)
    for i in range(length):
        password += random.choice(symbols_list)
    return password


class UserBase(BaseModel):
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    email: str
    phone: Optional[str] = None
    experience: Optional[int] = None
    city: Optional[str] = None
    role: Roles = Roles.customer
    birthdate: Optional[datetime] = None
    about: Optional[str] = None
    created_date: datetime
    contact_time: Optional[str]

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str = generate_pwd()
    created_date: datetime = datetime.utcnow()

    @validator('password')
    def valid_password(cls, v: str):
        if len(v) < 6:
            raise ValueError('Password should be at least 6 characters')
        return v


class UserDB(UserBase):
    id: UUID
    password: str


class UserUpdate(UserCreate):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    role: Optional[Roles]
    created_date: Optional[datetime]
    password: Optional[str]


class SocialMediaBase(BaseModel):
    link: str
    type: SocialMediaType


class SocialMediaDB(SocialMediaBase):
    id: UUID
    user_id: UUID

    class Config:
        orm_mode = True


class SocialMediaCreate(SocialMediaBase):
    user_id: UUID


class SocialMediaUpdate(SocialMediaCreate):
    user_id: Optional[UUID]
    link: Optional[str]
    type: Optional[SocialMediaType]


class TagsBase(BaseModel):
    name: str


class TagsDB(TagsBase):
    id: UUID

    class Config:
        orm_mode = True


class TagsCreate(TagsBase):
    pass


class TagsUpdate(TagsCreate):
    name: Optional[str]


class UserTagsBase(BaseModel):
    user_id: UUID
    tag_id: UUID


class UserTagsDB(UserTagsBase):
    pass

    class Config:
        orm_mode = True


class UserTagsCreate(UserTagsBase):
    pass


class UserTagsUpdate(UserTagsCreate):
    user_id: Optional[UUID]
    tag_id: Optional[UUID]


class PriceListBase(BaseModel):
    user_id: Optional[UUID]
    service: str
    price: int


class PriceListDB(PriceListBase):
    id: UUID

    class Config:
        orm_mode = True


class PriceListCreate(PriceListBase):
    pass


class PriceListUpdate(PriceListCreate):
    service: Optional[str]
    price: Optional[str]


class FeedbackBase(BaseModel):
    text: str
    author_id: UUID
    photographer_id: UUID
    created_date: datetime
    updated_date: datetime


class FeedbackDB(FeedbackBase):
    id: UUID
    created_date: datetime = datetime.utcnow()

    class Config:
        orm_mode = True


class FeedbackCreate(FeedbackBase):
    pass


class FeedbackUpdate(FeedbackCreate):
    text: Optional[str]
    author_id: Optional[UUID]
    photographer_id: Optional[UUID]
    updated_date: datetime = datetime.utcnow()
