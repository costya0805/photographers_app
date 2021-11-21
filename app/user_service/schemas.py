from datetime import datetime
import random
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, validator

from app.user_service.models import Roles


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
    birthdate: Optional[datetime] = None
    city: Optional[str] = None
    role: Roles = Roles.customer
    creation_date: datetime

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str = generate_pwd()
    creation_date: datetime = datetime.utcnow()

    @validator('password')
    def valid_password(cls, v: str):
        if len(v) < 6:
            raise ValueError('Password should be at least 6 characters')
        return v


class UserDB(UserBase):
    id: UUID
    password: str
