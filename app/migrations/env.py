import asyncio
# from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool
from sqlalchemy.ext.asyncio import AsyncEngine


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
# fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
# target_metadata = None
from app.db import Base
from app.user_service import models
from app.ordering_service import models

target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = AsyncEngine(
        engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
            future=True,
        )
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


if context.is_offline_mode():
    run_migrations_offline()
else:
    # asyncio.run(run_migrations_online())
    # loop = asyncio.get_event_loop()
    loop = asyncio.get_event_loop()
    if loop.is_running():
        asyncio.create_task(run_migrations_online())
    else:
        asyncio.run(run_migrations_online())
    # try:
    #     loop = asyncio.get_running_loop()
    # except RuntimeError:
    #     loop = None
    # if loop and loop.is_running():
    #     loop.run_until_complete(run_migrations_online())
    # else:
    #     asyncio.run(run_migrations_online())
    # loop.run_in_executor(None, run_migrations_online)
    # try:
    #     loop = asyncio.get_running_loop()
    # except RuntimeError:
    #     loop = None
    #
    # if loop and loop.is_running():
    #     tsk = loop.create_task(run_migrations_online())
    #     tsk.add_done_callback(  # optional
    #         lambda t: print(f'Task done: '  # optional
    #                         f'{t.result()=} << return val of main()'))  # optional (using py38)
    # else:
    #     print('Starting new event loop')
    #     asyncio.run(run_migrations_online())

