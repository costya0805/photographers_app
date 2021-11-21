from datetime import datetime
from typing import Optional

from ..models import Roles
from ..schemas import UserBase, UserDB, UserCreate


class Admin(UserBase):
    role: Roles = Roles.admin


class AdminDB(Admin, UserDB):
    pass


class AdminCreate(Admin, UserCreate):
    role: Optional[Roles] = Roles.admin


class AdminUpdate(AdminCreate):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    role: Optional[Roles]
    password: Optional[str]
    creation_date: Optional[datetime]
