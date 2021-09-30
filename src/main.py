from fastapi import FastAPI, Depends
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from .db import get_db, init_models
from .photos.add_photo import add_photo
from .photos.data import my_photos
from .users.models import UserModel
from .users.schemas import UserSchema

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    await init_models()


@app.get("/")
async def read_root():
    return {"Hello": "World", "Version": "1.2"}


@app.get("/photos")
async def read_item():
    return {"photos": my_photos}


@app.get("/photos/{photo_id}")
async def read_item(photo_id: int):
    return {"photo": my_photos[photo_id]}


@app.post("/photos")
async def post_item(photo_id: int, description: str):
    await add_photo(photo_id, description)
    return {"photos": my_photos}


@app.post("/user/", response_model=UserSchema)
async def create_user(user: UserSchema, db: AsyncSession = Depends(get_db)):
    new_user = UserModel(
        first_name=user.first_name, last_name=user.last_name, age=user.age
    )
    db.add(new_user)
    try:
        await db.commit()
        return new_user
    except IntegrityError:
        await db.rollback()
        raise Exception("User already exist")


@app.get("/user/", response_model=UserSchema)
async def get_user(first_name: str, db: AsyncSession = Depends(get_db)):
    user = await db.execute(select(UserModel).filter_by(first_name=first_name))
    return user.scalars().first()
