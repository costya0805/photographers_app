from typing import Optional

from ..models import Roles
from ..schemas import UserBase, UserDB, UserCreate


class Customer(UserBase):
    pass


class CustomerDB(Customer, UserDB):
    pass


class CustomerCreate(Customer, UserCreate):
    pass


class CustomerUpdate(CustomerCreate):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    role: Optional[Roles]
    password: Optional[str]
