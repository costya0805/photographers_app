import logging
from typing import List
from uuid import UUID
from .user_service.auth import get_current_user

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from .db import async_db_session
from .user_service.models_api import TagsAPI, UserAPI
from .user_service.routers import router as user_router
from .ordering_service.routers import router as order_router
from .user_service.schemas import TagsBase, TagsCreate, TagsDB, UserDB

app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://eshoot.herokuapp.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


logger = logging.getLogger(__name__)
user_api = UserAPI()
tags_api = TagsAPI()


app.include_router(user_router, prefix='/users', tags=['Users'])
app.include_router(order_router, prefix='/users', tags=['Orders'])  # путь до заказов: /users/user_id/orders


@app.get("/")
async def read_root():
    return {"Hello": "World", "Version": "4"}


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(async_db_session)):
    user: UserDB = await user_api.get_user_by_email(db, form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    password = form_data.password
    if not password == user.password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.email, "token_type": "bearer"}
    
@app.post("/tag", response_model = List[TagsDB])
async def create_tag(
        tags: List[TagsBase],
        db: AsyncSession = Depends(async_db_session), 
        current_user: UserDB = Depends(get_current_user)
):
    tags = [TagsCreate(**tag.dict()) for tag in tags]
    return await tags_api.create_tags(db, tags)

@app.get("/tags", response_model = List[TagsDB])
async def tags(
        db: AsyncSession = Depends(async_db_session)
):
    return await tags_api.get_tags(db)

@app.delete("/tag/{tag_id}")
async def delete_tag(
        tag_id: UUID,
        db: AsyncSession = Depends(async_db_session),
        current_user: UserDB = Depends(get_current_user)
):
    return await tags_api.delete_tag(db, tag_id)