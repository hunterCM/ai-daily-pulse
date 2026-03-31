from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.database import get_db
from app.models import Article, DailyBrief, Subscriber
from app.schemas import ArticleResponse, StatsResponse
from app.services.scheduler import generate_and_send_brief

router = APIRouter(prefix="/api", tags=["news"])


@router.get("/articles", response_model=list[ArticleResponse])
def list_articles(
    skip: int = 0,
    limit: int = 50,
    source: str | None = None,
    category: str | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(Article).order_by(desc(Article.fetched_at))
    if source:
        query = query.filter(Article.source.contains(source))
    if category:
        query = query.filter(Article.category == category)
    return query.offset(skip).limit(limit).all()


@router.get("/stats", response_model=StatsResponse)
def get_stats(db: Session = Depends(get_db)):
    total_subscribers = db.query(Subscriber).filter(Subscriber.is_active.is_(True)).count()
    total_briefs = db.query(DailyBrief).count()
    total_articles = db.query(Article).count()
    latest = db.query(DailyBrief).order_by(desc(DailyBrief.date)).first()
    return StatsResponse(
        total_subscribers=total_subscribers,
        total_briefs=total_briefs,
        total_articles=total_articles,
        latest_brief_date=latest.date if latest else None,
    )


@router.post("/trigger-brief")
async def trigger_brief_manually():
    """Manually trigger brief generation (for testing)."""
    try:
        await generate_and_send_brief()
        return {"message": "Brief generation triggered successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Brief generation failed: {str(e)}")


@router.get("/sources")
def list_sources(db: Session = Depends(get_db)):
    sources = db.query(Article.source).distinct().all()
    return [s[0] for s in sources]


@router.get("/categories")
def list_categories(db: Session = Depends(get_db)):
    categories = db.query(Article.category).distinct().all()
    return [c[0] for c in categories if c[0]]
