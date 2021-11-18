from sqlalchemy import Column, Integer, String, Enum

from ..db import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, unique=True, index=True)
    last_name = Column(String)
    middle_name = Column(String)
    age = Column(Integer)
    email = Column(String)
    phone = Column(Integer)
    city = Column(Enum)

