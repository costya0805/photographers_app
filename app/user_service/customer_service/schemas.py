from datetime import datetime
from typing import Optional

from ..models import Roles
from ..schemas import UserBase, UserDB, UserCreate, UserUpdate


class Customer(UserBase):
    role: Roles = Roles.customer


class CustomerDB(Customer, UserDB):
    pass


class CustomerCreate(Customer, UserCreate):
    role: Optional[Roles] = Roles.customer


class CustomerUpdate(CustomerCreate, UserUpdate):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    role: Optional[Roles]
    password: Optional[str]
    created_date: Optional[datetime]
