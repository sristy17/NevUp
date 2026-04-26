from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db import SessionLocal
from app.models.trade import Trade
from app.auth.deps import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/trades")
def create_trade(trade: dict, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if trade["userId"] != user["sub"]:
        raise HTTPException(status_code=403, detail="FORBIDDEN")

    existing = db.query(Trade).filter(Trade.tradeId == trade["tradeId"]).first()

    if existing:
        return existing

    new_trade = Trade(**trade)
    db.add(new_trade)
    db.commit()
    db.refresh(new_trade)

    return new_trade