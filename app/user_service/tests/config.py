import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import async_db_session


@pytest.fixture()
async def db() -> AsyncSession:
    async with async_db_session as session:
        yield session
