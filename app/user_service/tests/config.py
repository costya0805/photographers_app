import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import async_db_session


@pytest.fixture()
def db() -> AsyncSession:
    print("SESSION START")
    async with async_db_session as session:
        yield session
    print("SESSION FINISH")
