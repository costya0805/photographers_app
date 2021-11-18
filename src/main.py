import logging

from fastapi import Depends, FastAPI
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from .db import async_db_session
from .photos.add_photo import add_photo
from .photos.data import my_photos
from .users.models import UserModel
from .users.schemas import UserSchema

app = FastAPI()


logger = logging.getLogger(__name__)


@app.get("/")
async def read_root():
    return {"Hello": "World", "Version": "1.3"}


@app.get("/photos")
async def read_item():
    return {"photos": my_photos}


@app.get("/photos/{photo_id}")
async def read_item(photo_id: int):
    return {"photo": my_photos[photo_id]}


@app.post("/photos")
async def post_item(photo_id: int, description: str):
    await add_photo(photo_id, description)
    logger.info(f"Added new photo with id={photo_id}")
    return {"photos": my_photos}


@app.post("/user/", response_model=UserSchema)
async def create_user(user: UserSchema, db: AsyncSession = Depends(async_db_session)):
    new_user = UserModel(
        first_name=user.first_name, last_name=user.last_name, age=user.age
    )
    db.add(new_user)
    try:
        await db.commit()
        return new_user
    except IntegrityError:
        await db.rollback()
        logger.error(f"User {user.first_name} already exist")
        raise Exception("User already exist")


@app.get("/user/", response_model=UserSchema)
async def get_user(first_name: str, db: AsyncSession = Depends(async_db_session)):
    user = await db.execute(select(UserModel).filter_by(first_name=first_name))
    return user.scalars().first()
