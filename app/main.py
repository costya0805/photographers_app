import logging

from fastapi import FastAPI

from .user_service.routers import router as user_router
from .ordering_service.routers import router as order_router

app = FastAPI()


logger = logging.getLogger(__name__)


app.include_router(user_router, prefix='/users', tags=['Users'])
app.include_router(order_router, prefix='/orders', tags=['Orders'])


@app.get("/")
async def read_root():
    return {"Hello": "World", "Version": "3"}
