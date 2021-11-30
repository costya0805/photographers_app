from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import CustomerUpdate, CustomerCreate, CustomerDB
from .service import get_customers, get_customer, create_customer, update_customer
from app.db import async_db_session

router = APIRouter()


@router.get("/", response_model=List[CustomerDB])
async def customers(db: AsyncSession = Depends(async_db_session)):
    return await get_customers(db)


@router.post("/", response_model=CustomerDB)
async def create_customer_account(customer: CustomerCreate, db: AsyncSession = Depends(async_db_session)):
    user = await create_customer(db, customer)
    return user


@router.get("/{user_id}", response_model=CustomerDB)
async def customer_account(user_id: UUID, db: AsyncSession = Depends(async_db_session)):
    return await get_customer(db, user_id)


@router.patch("/{user_id}", response_model=CustomerDB)
async def update_customer_account(
        user_id: UUID, customer: CustomerUpdate, db: AsyncSession = Depends(async_db_session)
):
    return await update_customer(db, user_id, customer)
