from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.database import get_db
from app.models import Subscriber
from app.schemas import SubscriberCreate, SubscriberResponse, MessageResponse

router = APIRouter(prefix="/api/subscribers", tags=["subscribers"])


@router.post("/", response_model=SubscriberResponse)
def subscribe(data: SubscriberCreate, db: Session = Depends(get_db)):
    existing = db.query(Subscriber).filter(Subscriber.email == data.email).first()
    if existing:
        if existing.is_active:
            raise HTTPException(status_code=400, detail="Email already subscribed")
        existing.is_active = True
        existing.unsubscribed_at = None
        existing.name = data.name or existing.name
        db.commit()
        db.refresh(existing)
        return existing

    subscriber = Subscriber(email=data.email, name=data.name)
    db.add(subscriber)
    db.commit()
    db.refresh(subscriber)
    return subscriber


@router.delete("/{email}", response_model=MessageResponse)
def unsubscribe(email: str, db: Session = Depends(get_db)):
    subscriber = db.query(Subscriber).filter(Subscriber.email == email).first()
    if not subscriber:
        raise HTTPException(status_code=404, detail="Subscriber not found")
    subscriber.is_active = False
    subscriber.unsubscribed_at = datetime.now(timezone.utc)
    db.commit()
    return MessageResponse(message="Successfully unsubscribed")


@router.get("/", response_model=list[SubscriberResponse])
def list_subscribers(db: Session = Depends(get_db)):
    return db.query(Subscriber).filter(Subscriber.is_active.is_(True)).all()


@router.get("/count")
def subscriber_count(db: Session = Depends(get_db)):
    count = db.query(Subscriber).filter(Subscriber.is_active.is_(True)).count()
    return {"count": count}
