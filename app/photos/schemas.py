from pydantic import BaseModel


class PhotoSchema(BaseModel):
    name: str
    width: int = 0
    height: int = 1

    class Config:
        orm_mode = True
