from datetime import datetime
import random
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

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

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str = generate_pwd()


class UserDB(UserBase):
    id: UUID
    password: str
