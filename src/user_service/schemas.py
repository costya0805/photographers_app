from pydantic import BaseModel


class UserSchema(BaseModel):
    first_name: str
    last_name: str = None
    age: int

    class Config:
        orm_mode = True
