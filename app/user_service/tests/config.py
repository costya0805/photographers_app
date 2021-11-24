import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import async_db_session, engine, Base, async_session


@pytest.fixture()
def db() -> AsyncSession:
    print("SESSION START")
    async with async_db_session as session:
        yield session
    print("SESSION FINISH")


@pytest.fixture()
async def db_session() -> AsyncSession:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)
        async with async_session(bind=connection) as session:
            yield session
            await session.flush()
            await session.rollback()
