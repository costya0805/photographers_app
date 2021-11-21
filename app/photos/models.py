from sqlalchemy import Column, Integer, String

from ..db import Base


class PhotoModel(Base):
    __tablename__ = "photos"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    width = Column(Integer)
    height = Column(Integer)
