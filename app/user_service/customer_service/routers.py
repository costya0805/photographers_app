from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import Customer, CustomerUpdate, CustomerCreate, CustomerDB
from .service import get_customers, get_customer, create_customer, update_customer
from app.db import async_db_session

router = APIRouter()


@router.get("/", response_model=List[Customer])
async def customers(db: AsyncSession = Depends(async_db_session)):
    users = await get_customers(db)
    return [Customer(**user.dict()) for user in users]


@router.post("/", response_model=CustomerDB)
async def create_customer_account(customer: CustomerCreate, db: AsyncSession = Depends(async_db_session)):
    user = await create_customer(db, customer)
    return user


@router.get("/{user_id}", response_model=Customer)
async def customer_account(user_id: UUID, db: AsyncSession = Depends(async_db_session)):
    user = await get_customer(db, user_id)
    return Customer(**dict(user))


@router.patch("/{user_id}", response_model=Customer)
async def update_customer_account(user_id: UUID, customer: CustomerUpdate, db: AsyncSession = Depends(async_db_session)):
    user = await update_customer(db, user_id, customer)
    return Customer(**user.dict())
