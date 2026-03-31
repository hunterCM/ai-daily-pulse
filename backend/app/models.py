from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base

brief_articles = Table(
    "brief_articles",
    Base.metadata,
    Column("brief_id", Integer, ForeignKey("daily_briefs.id"), primary_key=True),
    Column("article_id", Integer, ForeignKey("articles.id"), primary_key=True),
)


class Subscriber(Base):
    __tablename__ = "subscribers"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    unsubscribed_at = Column(DateTime, nullable=True)


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    url = Column(String(1000), nullable=False)
    source = Column(String(100), nullable=False)
    summary = Column(Text, nullable=True)
    score = Column(Integer, default=0)
    author = Column(String(255), nullable=True)
    published_at = Column(DateTime, nullable=True)
    fetched_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    category = Column(String(100), nullable=True)

    briefs = relationship("DailyBrief", secondary=brief_articles, back_populates="articles")


class DailyBrief(Base):
    __tablename__ = "daily_briefs"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, nullable=False, index=True)
    short_summary = Column(Text, nullable=True)
    full_summary = Column(Text, nullable=True)
    pdf_path = Column(String(500), nullable=True)
    sent = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    subscriber_count = Column(Integer, default=0)

    articles = relationship("Article", secondary=brief_articles, back_populates="briefs")
