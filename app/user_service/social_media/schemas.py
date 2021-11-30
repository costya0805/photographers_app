from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from app.user_service.models import SocialMediaType


class SocialMediaBase(BaseModel):
    link: str
    type: SocialMediaType


class SocialMediaDB(SocialMediaBase):
    id: UUID
    user_id: UUID

    class Config:
        orm_mode = True


class SocialMediaCreate(SocialMediaBase):
    user_id: UUID


class SocialMediaUpdate(SocialMediaCreate):
    user_id: Optional[UUID]
    link: Optional[str]
    type: Optional[SocialMediaType]
