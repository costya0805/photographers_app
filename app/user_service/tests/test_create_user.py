from datetime import datetime

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.user_service.admin_service.service import create_admin
from app.user_service.customer_service.service import create_customer
from app.user_service.customer_service.schemas import CustomerCreate, Customer
from app.user_service.models import Roles
from app.user_service.photographer_service.service import create_photographer
from app.user_service.photographer_service.schemas import PhotographerCreate, Photographer
from app.user_service.admin_service.schemas import AdminCreate, Admin


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "user,photographer",
    [
        (
                PhotographerCreate(
                    **{
                        'first_name': 'Man',
                        'last_name': 'Nowhere',
                        'middle_name': 'Middle',
                        'email': 'nowhere@man.com',
                        'phone': '+100',
                        'birthdate': datetime(year=2000, month=1, day=1),
                        'city': 'Nowhere',
                        'role': Roles.photographer,
                        'experience': 3,
                        'about': "Good man",
                        'created_date': datetime(year=2021, month=11, day=1)
                    }
                ),
                Photographer(
                    **{
                        'first_name': 'Man',
                        'last_name': 'Nowhere',
                        'middle_name': 'Middle',
                        'email': 'nowhere@man.com',
                        'phone': '+100',
                        'birthdate': datetime(year=2000, month=1, day=1),
                        'city': 'Nowhere',
                        'role': Roles.photographer,
                        'experience': 3,
                        'about': "Good man",
                        'created_date': datetime(year=2021, month=11, day=1)
                    }
                )
        ),
    ]
)
async def test_create_photographer(db_session: AsyncSession, user: PhotographerCreate, photographer: Photographer):
    user = await create_photographer(db_session, user)
    assert Photographer(**dict(user)) == photographer


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "user,customer",
    [
        (
                CustomerCreate(**{
                    'first_name': 'Man',
                    'last_name': 'Nowhere',
                    'middle_name': 'Middle',
                    'email': 'nowhere@man.com',
                    'phone': '+100',
                    'birthdate': datetime(year=2000, month=1, day=1),
                    'city': 'Nowhere',
                    'role': Roles.customer,
                    'created_date': datetime(year=2021, month=11, day=1)
                }),
                Customer(**{
                    'first_name': 'Man',
                    'last_name': 'Nowhere',
                    'middle_name': 'Middle',
                    'email': 'nowhere@man.com',
                    'phone': '+100',
                    'birthdate': datetime(year=2000, month=1, day=1),
                    'city': 'Nowhere',
                    'role': Roles.customer,
                    'created_date': datetime(year=2021, month=11, day=1)
                })
        ),
    ]
)
async def test_create_customer(db_session: AsyncSession, user: CustomerCreate, customer: Customer):
    user = await create_customer(db_session, user)
    assert Customer(**dict(user)) == customer


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "user,admin",
    [
        (
                AdminCreate(**{
                    'first_name': 'Man',
                    'last_name': 'Nowhere',
                    'middle_name': 'Middle',
                    'email': 'nowhere@man.com',
                    'phone': '+100',
                    'birthdate': datetime(year=2000, month=1, day=1),
                    'city': 'Nowhere',
                    'role': Roles.admin,
                    'created_date': datetime(year=2021, month=11, day=1)
                }),
                Admin(**{
                    'first_name': 'Man',
                    'last_name': 'Nowhere',
                    'middle_name': 'Middle',
                    'email': 'nowhere@man.com',
                    'phone': '+100',
                    'birthdate': datetime(year=2000, month=1, day=1),
                    'city': 'Nowhere',
                    'role': Roles.admin,
                    'created_date': datetime(year=2021, month=11, day=1)
                })
        ),
    ]
)
async def test_create_admin(db_session: AsyncSession, user: AdminCreate, admin: Admin):
    user = await create_admin(db_session, user)
    assert Admin(**dict(user)) == admin
