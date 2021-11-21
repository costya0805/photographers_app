import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.user_service.admin_service.service import create_admin, get_admin
from app.user_service.customer_service.service import create_customer, get_customer
from app.user_service.customer_service.schemas import CustomerCreate, Customer
from app.user_service.photographer_service.service import create_photographer, get_photographer
from app.user_service.photographer_service.schemas import PhotographerCreate, Photographer
from app.user_service.admin_service.schemas import AdminCreate, Admin


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
async def test_get_photographer(db: AsyncSession, user: PhotographerCreate, photographer: Photographer):
    user = await create_photographer(db, user)
    gotten_user = await get_photographer(db, user.id)
    assert Photographer(**dict(gotten_user)) == photographer


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
async def test_get_customer(db: AsyncSession, user: CustomerCreate, customer: Customer):
    user = await create_customer(db, user)
    gotten_user = await get_customer(db, user.id)
    assert Customer(**dict(gotten_user)) == customer


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
async def test_get_admin(db: AsyncSession, user: AdminCreate, admin: Admin):
    user = await create_admin(db, user)
    gotten_user = await get_admin(db, user.id)
    assert Admin(**dict(gotten_user)) == admin
