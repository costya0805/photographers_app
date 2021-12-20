import enum
import uuid

from sqlalchemy import Column, String, Enum, DateTime, ForeignKey, sql, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db import Base


class OrderStatus(enum.Enum):
    new = 'new'
    in_progress = 'in_progress'
    closed = 'closed'
    canceled = 'canceled'


class Order(Base):
    __tablename__ = "order"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    status = Column(Enum(OrderStatus), default=OrderStatus.new, nullable=False, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Integer, default=0)
    created_date = Column(DateTime(timezone=True), server_default=sql.func.now())
    updated_date = Column(DateTime(timezone=True))

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
