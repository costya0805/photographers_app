from fastapi import FastAPI
from .photos.add_photo import add_photo
from .photos.data import my_photos

app = FastAPI()


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
