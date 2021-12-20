from datetime import datetime

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.user_service.admin_service.service import create_admin, update_admin
from app.user_service.customer_service.service import create_customer, update_customer
from app.user_service.customer_service.schemas import CustomerCreate, Customer, CustomerUpdate
from app.user_service.models import Roles
from app.user_service.photographer_service.service import create_photographer, update_photographer
from app.user_service.photographer_service.schemas import PhotographerCreate, Photographer, PhotographerUpdate
from app.user_service.admin_service.schemas import AdminCreate, Admin, AdminUpdate


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "user,updated,photographer",
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
                PhotographerUpdate(**{
                    'middle_name': 'Smith',
                    'city': 'Moscow',
                }),
                Photographer(
                    **{
                        'first_name': 'Man',
                        'last_name': 'Nowhere',
                        'middle_name': 'Smith',
                        'email': 'nowhere@man.com',
                        'phone': '+100',
                        'birthdate': datetime(year=2000, month=1, day=1),
                        'city': 'Moscow',
                        'role': Roles.photographer,
                        'experience': 3,
                        'about': "Good man",
                        'created_date': datetime(year=2021, month=11, day=1)
                    }
                )
        ),
    ]
)
async def test_update_photographer(db_session: AsyncSession, user: PhotographerCreate, updated: PhotographerUpdate,
                                   photographer: Photographer):
    user = await create_photographer(db_session, user)
    updated_user = await update_photographer(db_session, user.id, updated)
    assert Photographer(**dict(updated_user)) == photographer


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "user,updated,customer",
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
                CustomerUpdate(**{
                    'middle_name': 'Smith',
                    'city': 'Moscow',
                }),
                Customer(**{
                    'first_name': 'Man',
                    'last_name': 'Nowhere',
                    'middle_name': 'Smith',
                    'email': 'nowhere@man.com',
                    'phone': '+100',
                    'birthdate': datetime(year=2000, month=1, day=1),
                    'city': 'Moscow',
                    'role': Roles.customer,
                    'created_date': datetime(year=2021, month=11, day=1)
                })
        ),
    ]
)
async def test_update_customer(db_session: AsyncSession, user: CustomerCreate, updated: CustomerUpdate, customer: Customer):
    user = await create_customer(db_session, user)
    updated_user = await update_customer(db_session, user.id, updated)
    assert Customer(**dict(updated_user)) == customer


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "user,updated,admin",
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
                AdminUpdate(**{
                    'middle_name': 'Smith',
                    'city': 'Moscow',
                }),
                Admin(**{
                    'first_name': 'Man',
                    'last_name': 'Nowhere',
                    'middle_name': 'Smith',
                    'email': 'nowhere@man.com',
                    'phone': '+100',
                    'birthdate': datetime(year=2000, month=1, day=1),
                    'city': 'Moscow',
                    'role': Roles.admin,
                    'created_date': datetime(year=2021, month=11, day=1)
                })
        ),
    ]
)
async def test_update_admin(db_session: AsyncSession, user: AdminCreate, updated: AdminUpdate, admin: Admin):
    user = await create_admin(db_session, user)
    updated_user = await update_admin(db_session, user.id, updated)
    assert Admin(**dict(updated_user)) == admin
