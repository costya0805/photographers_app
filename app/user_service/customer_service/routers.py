from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import CustomerUpdate, CustomerCreate, CustomerDB
from .service import get_customers, get_customer, create_customer, update_customer
from app.db import async_db_session
from ..auth import get_current_user, is_the_same_user
from ..schemas import UserDB

router = APIRouter()


@router.get("/", response_model=List[CustomerDB])
async def customers(db: AsyncSession = Depends(async_db_session), current_user: UserDB = Depends(get_current_user)):
    return await get_customers(db)


@router.post("/", response_model=CustomerDB)
async def create_customer_account(customer: CustomerCreate, db: AsyncSession = Depends(async_db_session)):
    user = await create_customer(db, customer)
    return user


@router.get("/{user_id}", response_model=CustomerDB)
async def customer_account(
        user_id: UUID, db: AsyncSession = Depends(async_db_session), current_user: UserDB = Depends(get_current_user)
):
    return await get_customer(db, user_id)


@router.patch("/{user_id}", response_model=CustomerDB)
async def update_customer_account(
        user_id: UUID,
        customer: CustomerUpdate,
        db: AsyncSession = Depends(async_db_session),
        current_user: UserDB = Depends(get_current_user)
):
    await is_the_same_user(user_id, current_user)
    return await update_customer(db, user_id, customer)
