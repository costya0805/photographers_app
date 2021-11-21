import logging

from fastapi import FastAPI

from .user_service.routers import router as user_router

app = FastAPI()


logger = logging.getLogger(__name__)


app.include_router(user_router, prefix='/users', tags=['Users'])


@app.get("/")
async def read_root():
    return {"Hello": "World", "Version": "2"}
