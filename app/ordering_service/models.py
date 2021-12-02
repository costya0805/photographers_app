import enum
import uuid

from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey, sql
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
    description = Column(String, nullable=False)
    price = Column(String, default=0)

    customer = relationship("User", cascade="all, delete")
    customer_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    performer = relationship("User", cascade="all, delete")
    performer_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    comments = relationship("Comment", cascade="all, delete")
    dates = relationship("Dates", cascade="all, delete")
    # attachments = fore


class Comment(Base):
    __tablename__ = "comment"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    text = Column(String, nullable=False)
    author = relationship("User")
    author_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    order_id = Column(UUID(as_uuid=True), ForeignKey("order.id"), nullable=False)
    creation_date = Column(DateTime(timezone=True), server_default=sql.func.now())


class Dates(Base):
    __tablename__ = "dates"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    description = Column(String, nullable=False)
    start_datetime = Column(DateTime(timezone=True), nullable=False)
    end_datetime = Column(DateTime(timezone=True), nullable=False)
    order_id = Column(UUID(as_uuid=True), ForeignKey("order.id"), nullable=False)
