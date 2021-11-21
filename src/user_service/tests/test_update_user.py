import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.user_service.admin_service.service import create_admin, update_admin
from src.user_service.customer_service.service import create_customer, update_customer
from src.user_service.customer_service.schemas import CustomerCreate, Customer, CustomerUpdate
from src.user_service.photographer_service.service import create_photographer, update_photographer
from src.user_service.photographer_service.schemas import PhotographerCreate, Photographer, PhotographerUpdate
from src.user_service.admin_service.schemas import AdminCreate, Admin, AdminUpdate


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "user,updated,photographer",
    [
        (PhotographerCreate(**{
            'first_name': 'Man',
            'second_name': 'Nowhere',
            'age': 20
        }),
         PhotographerUpdate(**{
             'second_name': 'Smith',
             'age': 21
         }),
         Photographer(**{
             'first_name': 'Man',
             'second_name': 'Smith',
             'age': 21
         })),
    ]
)
async def test_update_photographer(db: AsyncSession, user: PhotographerCreate, updated: PhotographerUpdate, photographer: Photographer):
    user = await create_photographer(db, user)
    updated_user = await update_photographer(db, user.id, updated)
    assert Photographer(**dict(updated_user)) == photographer


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "user,updated,customer",
    [
        (CustomerCreate(**{
            'first_name': 'Man',
            'second_name': 'Nowhere',
            'age': 20
        }),
         CustomerUpdate(**{
             'second_name': 'Smith',
             'age': 21
         }),
         Customer(**{
             'first_name': 'Man',
             'second_name': 'Smith',
             'age': 21
         })),
    ]
)
async def test_update_customer(db: AsyncSession, user: CustomerCreate, updated: CustomerUpdate, customer: Customer):
    user = await create_customer(db, user)
    updated_user = await update_customer(db, user.id, updated)
    assert Customer(**dict(updated_user)) == customer


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "user,updated,admin",
    [
        (AdminCreate(**{
            'first_name': 'Man',
            'second_name': 'Nowhere',
            'age': 20
        }),
         AdminUpdate(**{
             'second_name': 'Smith',
             'age': 21
         }),
         Admin(**{
             'first_name': 'Man',
             'second_name': 'Smith',
             'age': 21
         })),
    ]
)
async def test_update_admin(db: AsyncSession, user: AdminCreate, updated: AdminUpdate, admin: Admin):
    user = await create_admin(db, user)
    updated_user = await update_admin(db, user.id, updated)
    assert Admin(**dict(updated_user)) == admin
