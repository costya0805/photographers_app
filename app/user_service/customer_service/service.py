import logging
from typing import List
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import CustomerDB, CustomerCreate, CustomerUpdate
from ..models import Roles
from ..models_api import UserAPI

logger = logging.getLogger(__name__)
customer = UserAPI(Roles.customer, CustomerDB, CustomerCreate, CustomerUpdate)


async def get_customers(db: AsyncSession) -> List[CustomerDB]:
    customers: List[CustomerDB] = await customer.get_users(db)
    return customers


async def get_customer(db: AsyncSession, user_id: UUID) -> CustomerDB:
    gotten_customer: CustomerDB = await customer.get_user(db, user_id)
    return gotten_customer


async def create_customer(db: AsyncSession, user: CustomerCreate) -> CustomerDB:
    created_customer: CustomerDB = await customer.create_user(db, user)
    return created_customer


async def update_customer(db: AsyncSession, user_id: UUID, user: CustomerUpdate) -> CustomerDB:
    updated_customer: CustomerDB = await customer.update_user(db, user_id, user)
    return updated_customer
