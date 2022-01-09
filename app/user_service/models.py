import enum
import uuid

from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey, sql
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db import Base


class SocialMediaType(enum.Enum):
    vk = "VK"
    fb = "Facebook"
    inst = "Instagram"
    tg = "Telegram"
    tw = "Twitter"
    wa = "WhatsApp"
    vb = "Viber"
    web = "Web"


class Roles(enum.Enum):
    photographer = "Photographer"
    customer = "Customer"
    admin = "Admin"


class User(Base):
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    middle_name = Column(String)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    phone = Column(String)
    experience = Column(Integer)
    city = Column(String)
    role = Column(Enum(Roles), default=Roles.customer, nullable=False, index=True)
    birthdate = Column(DateTime(timezone=True), nullable=False)
    about = Column(String)
    created_date = Column(DateTime(timezone=True), server_default=sql.func.now())
    contact_time = Column(String)

    social_media = relationship("SocialMedia", cascade="all, delete")
    tags = relationship("UserTags", cascade="all, delete")
    price_list = relationship("PriceList", cascade="all, delete")
    feedbacks = relationship("Feedbacks", foreign_keys='Feedbacks.photographer_id', cascade="all, delete")
    # portfolios = relationship("Portfolio", cascade="all, delete")


class SocialMedia(Base):
    __tablename__ = "social media"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    link = Column(String, nullable=False)
    type = Column(Enum(SocialMediaType), nullable=False)


class Tags(Base):
    __tablename__ = "tags"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False)


class UserTags(Base):
    __tablename__ = "user tags"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    tag_id = Column(UUID(as_uuid=True), ForeignKey("tags.id"), nullable=False)


class PriceList(Base):
    __tablename__ = "price list"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    service = Column(String, nullable=False)
    price = Column(Integer, nullable=False)


class Feedbacks(Base):
    __tablename__ = "feedbacks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    text = Column(String, nullable=False)
    author_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    photographer_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    created_date = Column(DateTime(timezone=True), server_default=sql.func.now())
    updated_date = Column(DateTime(timezone=True))
