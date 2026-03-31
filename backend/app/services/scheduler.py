import logging
from datetime import datetime, timezone
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy.orm import Session
from app.config import get_settings
from app.database import SessionLocal
from app.models import Subscriber, Article, DailyBrief
from app.services.news_aggregator import aggregate_all_news
from app.services.summarizer import summarize_articles
from app.services.pdf_generator import generate_brief_pdf
from app.services.email_service import send_daily_brief

logger = logging.getLogger(__name__)
settings = get_settings()

scheduler = AsyncIOScheduler()


async def generate_and_send_brief():
    """Main pipeline: fetch news -> summarize -> generate PDF -> email subscribers."""
    logger.info("Starting daily brief generation pipeline...")
    db: Session = SessionLocal()

    try:
        articles_data = await aggregate_all_news()
        if not articles_data:
            logger.warning("No articles fetched — skipping brief generation")
            return

        db_articles = []
        for a in articles_data:
            article = Article(
                title=a["title"],
                url=a["url"],
                source=a["source"],
                summary=a.get("summary", ""),
                score=a.get("score", 0),
                author=a.get("author", ""),
                published_at=a.get("published_at"),
                category=a.get("category", ""),
            )
            db.add(article)
            db_articles.append(article)
        db.commit()
        logger.info(f"Saved {len(db_articles)} articles to database")

        summaries = await summarize_articles(articles_data)
        now = datetime.now(timezone.utc)
        pdf_path = generate_brief_pdf(summaries["full_summary"], articles_data, now)

        subscribers = db.query(Subscriber).filter(Subscriber.is_active.is_(True)).all()
        subscriber_emails = [s.email for s in subscribers]

        if not subscriber_emails:
            subscriber_emails = [settings.admin_email]

        brief = DailyBrief(
            date=now,
            short_summary=summaries["short_summary"],
            full_summary=summaries["full_summary"],
            pdf_path=pdf_path,
            subscriber_count=len(subscriber_emails),
        )
        db.add(brief)

        for article in db_articles:
            brief.articles.append(article)

        subject = f"AI Daily Pulse — {now.strftime('%B %d, %Y')}"
        sent = send_daily_brief(subscriber_emails, subject, summaries["short_summary"], pdf_path)
        brief.sent = sent

        db.commit()
        logger.info(f"Brief #{brief.id} generated and {'sent' if sent else 'saved (not sent)'} "
                     f"to {len(subscriber_emails)} subscribers")

    except Exception as e:
        logger.error(f"Brief generation pipeline failed: {e}", exc_info=True)
        db.rollback()
    finally:
        db.close()


def start_scheduler():
    trigger = CronTrigger(
        hour=settings.brief_hour,
        minute=settings.brief_minute,
        timezone=settings.timezone,
    )
    scheduler.add_job(
        generate_and_send_brief,
        trigger=trigger,
        id="daily_brief",
        name="Generate and Send Daily Brief",
        replace_existing=True,
    )
    scheduler.start()
    logger.info(
        f"Scheduler started — daily brief at {settings.brief_hour:02d}:{settings.brief_minute:02d} "
        f"{settings.timezone}"
    )


def stop_scheduler():
    if scheduler.running:
        scheduler.shutdown()
        logger.info("Scheduler stopped")
