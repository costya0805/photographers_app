import enum
import uuid

from sqlalchemy import Column, String, Enum, DateTime, Date, Time, ForeignKey, sql, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db import Base


class OrderStatus(enum.Enum):
    new = 'new'
    in_progress = 'in_progress'
    closed = 'closed'
    canceled = 'canceled'


class PageOrientation(enum.Enum):
    portrait = 'portrait'
    landscape = 'landscape'


class PageProportions(enum.Enum):
    one_to_one = '1x1'
    two_to_three = '2x3'
    three_to_four = '3x4'
    sixteen_to_nine = '16x9'


class FileFormat(enum.Enum):
    jpg = 'jpg'
    png = 'png'
    raw = 'raw'
    tiff = 'tiff'


class PostProcessing(enum.Enum):
    removing_defects = 'removing defects'
    color_correction = 'color correction'


class Order(Base):
    __tablename__ = "order"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    status = Column(Enum(OrderStatus), default=OrderStatus.new, nullable=False, index=True)
    type = Column(String, nullable=False)
    subtype = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Integer, nullable=True)
    barter = Column(String, nullable=True)
    created_date = Column(DateTime(timezone=True), server_default=sql.func.now())
    updated_date = Column(DateTime(timezone=True))
    date = Column(Date)
    start_time = Column(Time(timezone=True))
    end_time = Column(Time(timezone=True))
    deadline = Column(DateTime(timezone=True))
    address = Column(String)
    models = Column(String)
    number_of_frames = Column(Integer)
    screen_resolution = Column(String)
    orientation = Column(Enum(PageOrientation), default=PageOrientation.portrait, nullable=False)
    proportions = Column(Enum(PageProportions), default=PageProportions.one_to_one, nullable=False)
    file_format = Column(Enum(FileFormat), default=FileFormat.jpg, nullable=False)
    post_processing = Column(Enum(PostProcessing), default=PostProcessing.removing_defects, nullable=False)

    customer_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    performer_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)


class Comment(Base):
    __tablename__ = "comment"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    text = Column(String, nullable=False)
    author_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    order_id = Column(UUID(as_uuid=True), ForeignKey("order.id"), nullable=False)
    created_date = Column(DateTime(timezone=True), server_default=sql.func.now())
    updated_date = Column(DateTime(timezone=True))

    author = relationship("User")


class Dates(Base):
    __tablename__ = "dates"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    description = Column(String, nullable=False)
    start_datetime = Column(DateTime(timezone=True), nullable=False)
    end_datetime = Column(DateTime(timezone=True), nullable=False)

    order_id = Column(UUID(as_uuid=True), ForeignKey("order.id"), nullable=False)
