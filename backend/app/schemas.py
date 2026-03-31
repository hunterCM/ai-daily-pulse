from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class SubscriberCreate(BaseModel):
    email: EmailStr
    name: Optional[str] = None


class SubscriberResponse(BaseModel):
    id: int
    email: str
    name: Optional[str]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class ArticleResponse(BaseModel):
    id: int
    title: str
    url: str
    source: str
    summary: Optional[str]
    score: int
    author: Optional[str]
    published_at: Optional[datetime]
    fetched_at: datetime
    category: Optional[str]

    class Config:
        from_attributes = True


class BriefResponse(BaseModel):
    id: int
    date: datetime
    short_summary: Optional[str]
    full_summary: Optional[str]
    sent: bool
    created_at: datetime
    subscriber_count: int
    articles: list[ArticleResponse] = []

    class Config:
        from_attributes = True


class BriefListResponse(BaseModel):
    id: int
    date: datetime
    short_summary: Optional[str]
    sent: bool
    created_at: datetime
    article_count: int = 0

    class Config:
        from_attributes = True


class StatsResponse(BaseModel):
    total_subscribers: int
    total_briefs: int
    total_articles: int
    latest_brief_date: Optional[datetime]


class MessageResponse(BaseModel):
    message: str
