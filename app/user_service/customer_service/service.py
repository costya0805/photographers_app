from typing import List
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import CustomerDB, CustomerCreate, CustomerUpdate


async def get_customers(db: AsyncSession) -> List[CustomerDB]:
    pass


async def get_customer(db: AsyncSession, user_id: UUID) -> CustomerDB:
    pass


async def create_customer(db: AsyncSession, user: CustomerCreate) -> CustomerDB:
    pass


async def update_customer(db: AsyncSession, user_id: UUID, customer: CustomerUpdate) -> CustomerDB:
    pass
