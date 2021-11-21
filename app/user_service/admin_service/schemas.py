from typing import Optional

from ..models import Roles
from ..schemas import UserBase, UserDB, UserCreate


class Admin(UserBase):
    pass


class AdminDB(Admin, UserDB):
    pass


class AdminCreate(Admin, UserCreate):
    pass


class AdminUpdate(AdminCreate):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    role: Optional[Roles]
    password: Optional[str]
