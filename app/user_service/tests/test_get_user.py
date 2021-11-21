from datetime import datetime

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.user_service.admin_service.service import create_admin, get_admin
from app.user_service.customer_service.service import create_customer, get_customer
from app.user_service.customer_service.schemas import CustomerCreate, Customer
from app.user_service.models import Roles
from app.user_service.photographer_service.service import create_photographer, get_photographer
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
                        'creation_date': datetime(year=2021, month=11, day=1)
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
                        'creation_date': datetime(year=2021, month=11, day=1)
                    }
                )
        ),
        (
                PhotographerCreate(
                    **{
                        'first_name': 'Man',
                        'last_name': 'Nowhere',
                        'email': 'nowhere@man.com',
                        'creation_date': datetime(year=2021, month=11, day=1)
                    }
                ),
                Photographer(
                    **{
                        'first_name': 'Man',
                        'last_name': 'Nowhere',
                        'middle_name': None,
                        'email': 'nowhere@man.com',
                        'phone': None,
                        'birthdate': None,
                        'city': None,
                        'role': Roles.photographer,
                        'experience': 0,
                        'about': None,
                        'creation_date': datetime(year=2021, month=11, day=1)
                    }
                )
        ),
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
                    'creation_date': datetime(year=2021, month=11, day=1)
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
                    'creation_date': datetime(year=2021, month=11, day=1)
                })
        ),
        (
                CustomerCreate(**{
                    'first_name': 'Man',
                    'last_name': 'Nowhere',
                    'email': 'nowhere@man.com',
                    'creation_date': datetime(year=2021, month=11, day=1)
                }),
                Customer(**{
                    'first_name': 'Man',
                    'last_name': 'Nowhere',
                    'middle_name': None,
                    'email': 'nowhere@man.com',
                    'phone': None,
                    'birthdate': None,
                    'city': None,
                    'role': Roles.customer,
                    'experience': 0,
                    'about': None,
                    'creation_date': datetime(year=2021, month=11, day=1)
                })
        ),
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
                    'creation_date': datetime(year=2021, month=11, day=1)
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
                    'creation_date': datetime(year=2021, month=11, day=1)
                })
        ),
        (
                AdminCreate(**{
                    'first_name': 'Man',
                    'last_name': 'Nowhere',
                    'email': 'nowhere@man.com',
                    'creation_date': datetime(year=2021, month=11, day=1)
                }),
                Admin(**{
                    'first_name': 'Man',
                    'last_name': 'Nowhere',
                    'middle_name': None,
                    'email': 'nowhere@man.com',
                    'phone': None,
                    'birthdate': None,
                    'city': None,
                    'role': Roles.admin,
                    'experience': 0,
                    'about': None,
                    'creation_date': datetime(year=2021, month=11, day=1)
                })
        ),
    ]
)
async def test_get_admin(user: AdminCreate, admin: Admin, db: AsyncSession):
    user = await create_admin(db, user)
    gotten_user = await get_admin(db, user.id)
    assert Admin(**dict(gotten_user)) == admin
