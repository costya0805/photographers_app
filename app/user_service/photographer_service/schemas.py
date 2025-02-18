from datetime import datetime
from typing import Optional, List

from ..models import Roles
from ..schemas import BusyDatesDB, PortfolioDB, PortfolioPhotoDB, SocialMediaDB, UserBase, UserDB, UserCreate, SocialMediaCreate, TagsCreate, PriceListCreate, FeedbackCreate, \
    TagsDB, PriceListDB, FeedbackDB, UserUpdate


class Photographer(UserBase):
    role: Roles = Roles.photographer
    about: Optional[str] = None


class PhotographerDB(Photographer, UserDB):
    pass


class PhotographerCreate(Photographer, UserCreate):
    role: Optional[Roles] = Roles.photographer


class PhotographerUpdate(PhotographerCreate, UserUpdate):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    role: Optional[Roles]
    password: Optional[str]
    created_date: Optional[datetime]


class FullPhotographerCreate(PhotographerCreate):
    social_medias: List[SocialMediaCreate] = []
    tags: List[TagsCreate] = []
    price_list: List[PriceListCreate] = []


class PhotographerFullDB(PhotographerDB):
    tags: List[TagsDB] = []
    price_list: List[PriceListDB] = []
    feedbacks: List[FeedbackDB] = []
    social_medias: List[SocialMediaDB] = []
    portfolios: List[PortfolioDB] = []
    photos: List[PortfolioPhotoDB] = []
    busy_dates: List[BusyDatesDB] = []