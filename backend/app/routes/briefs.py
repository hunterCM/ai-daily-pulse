from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import desc
import os
from app.database import get_db
from app.models import DailyBrief
from app.schemas import BriefResponse, BriefListResponse

router = APIRouter(prefix="/api/briefs", tags=["briefs"])


@router.get("/", response_model=list[BriefListResponse])
def list_briefs(skip: int = 0, limit: int = 30, db: Session = Depends(get_db)):
    briefs = (
        db.query(DailyBrief)
        .order_by(desc(DailyBrief.date))
        .offset(skip)
        .limit(limit)
        .all()
    )
    results = []
    for brief in briefs:
        results.append(BriefListResponse(
            id=brief.id,
            date=brief.date,
            short_summary=brief.short_summary,
            sent=brief.sent,
            created_at=brief.created_at,
            article_count=len(brief.articles),
        ))
    return results


@router.get("/latest", response_model=BriefResponse)
def get_latest_brief(db: Session = Depends(get_db)):
    brief = db.query(DailyBrief).order_by(desc(DailyBrief.date)).first()
    if not brief:
        raise HTTPException(status_code=404, detail="No briefs found")
    return brief


@router.get("/{brief_id}", response_model=BriefResponse)
def get_brief(brief_id: int, db: Session = Depends(get_db)):
    brief = db.query(DailyBrief).filter(DailyBrief.id == brief_id).first()
    if not brief:
        raise HTTPException(status_code=404, detail="Brief not found")
    return brief


@router.get("/{brief_id}/pdf")
def download_brief_pdf(brief_id: int, db: Session = Depends(get_db)):
    brief = db.query(DailyBrief).filter(DailyBrief.id == brief_id).first()
    if not brief:
        raise HTTPException(status_code=404, detail="Brief not found")
    if not brief.pdf_path or not os.path.exists(brief.pdf_path):
        raise HTTPException(status_code=404, detail="PDF not available")
    return FileResponse(
        brief.pdf_path,
        media_type="application/pdf",
        filename=os.path.basename(brief.pdf_path),
    )
