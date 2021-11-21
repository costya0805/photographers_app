import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.user_service.admin_service.service import create_admin
from src.user_service.customer_service.service import create_customer
from src.user_service.customer_service.schemas import CustomerCreate, Customer
from src.user_service.photographer_service.service import create_photographer
from src.user_service.photographer_service.schemas import PhotographerCreate, Photographer
from src.user_service.admin_service.schemas import AdminCreate, Admin


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "user,photographer",
    [
        (PhotographerCreate(**{
            'first_name': 'Man',
            'second_name': 'Nowhere',
            'age': 20
        }),
         Photographer(**{
             'first_name': 'Man',
             'second_name': 'Nowhere',
             'age': 20
         })),
    ]
)
async def test_create_photographer(db: AsyncSession, user: PhotographerCreate, photographer: Photographer):
    user = await create_photographer(db, user)
    assert Photographer(**dict(user)) == photographer


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "user,customer",
    [
        (CustomerCreate(**{
            'first_name': 'Man',
            'second_name': 'Nowhere',
            'age': 20
        }),
         Customer(**{
             'first_name': 'Man',
             'second_name': 'Nowhere',
             'age': 20
         })),
    ]
)
async def test_create_customer(db: AsyncSession, user: CustomerCreate, customer: Customer):
    user = await create_customer(db, user)
    assert Customer(**dict(user)) == customer


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "user,admin",
    [
        (AdminCreate(**{
            'first_name': 'Man',
            'second_name': 'Nowhere',
            'age': 20
        }),
         Admin(**{
             'first_name': 'Man',
             'second_name': 'Nowhere',
             'age': 20
         })),
    ]
)
async def test_create_admin(db: AsyncSession, user: AdminCreate, admin: Admin):
    user = await create_admin(db, user)
    assert Admin(**dict(user)) == admin
