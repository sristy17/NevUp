from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db import SessionLocal
from app.models.trade import Trade
from app.auth.deps import get_current_user
from collections import defaultdict
from datetime import datetime, timedelta

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/users/{userId}/metrics")
def get_metrics(userId: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if user["sub"] != userId:
        raise HTTPException(status_code=403, detail="FORBIDDEN")

    trades = db.query(Trade).filter(Trade.userId == userId).all()
    trades = sorted(trades, key=lambda x: x.entryAt)

    total = len(trades)

    wins = 0
    for t in trades:
        if t.exitPrice and t.entryPrice and t.exitPrice > t.entryPrice:
            wins += 1

    last_10 = trades[-10:]
    adherence_values = [t.planAdherence for t in last_10 if t.planAdherence is not None]

    avg_adherence = 0
    if adherence_values:
        avg_adherence = sum(adherence_values) / len(adherence_values)

    revenge_count = 0

    for i in range(1, len(trades)):
        prev = trades[i - 1]
        curr = trades[i]

        if prev.exitPrice and prev.entryPrice and prev.exitPrice < prev.entryPrice:
            prev_time = datetime.fromisoformat(prev.exitAt.replace("Z", "+00:00"))
            curr_time = datetime.fromisoformat(curr.entryAt.replace("Z", "+00:00"))

            diff = (curr_time - prev_time).total_seconds()

            if diff <= 90 and curr.emotionalState in ["anxious", "fearful"]:
                revenge_count += 1

    session_data = defaultdict(list)

    for t in trades:
        session_data[t.sessionId].append(t)

    session_tilt = {}

    for session_id, session_trades in session_data.items():
        session_trades = sorted(session_trades, key=lambda x: x.entryAt)

        loss_following = 0

        for i in range(1, len(session_trades)):
            prev = session_trades[i - 1]

            if prev.exitPrice and prev.entryPrice and prev.exitPrice < prev.entryPrice:
                loss_following += 1

        total_session_trades = len(session_trades)

        tilt = 0
        if total_session_trades > 0:
            tilt = loss_following / total_session_trades

        session_tilt[session_id] = tilt

    emotion_stats = {}

    for t in trades:
        if not t.emotionalState:
            continue

        if t.emotionalState not in emotion_stats:
            emotion_stats[t.emotionalState] = {"wins": 0, "total": 0}

        emotion_stats[t.emotionalState]["total"] += 1

        if t.exitPrice and t.entryPrice and t.exitPrice > t.entryPrice:
            emotion_stats[t.emotionalState]["wins"] += 1

    emotion_winrate = {}

    for emotion, stats in emotion_stats.items():
        total_e = stats["total"]
        wins_e = stats["wins"]

        winrate = 0
        if total_e > 0:
            winrate = wins_e / total_e

        emotion_winrate[emotion] = winrate

    overtrading = False

    for i in range(len(trades)):
        start_time = datetime.fromisoformat(trades[i].entryAt.replace("Z", "+00:00"))
        count = 1

        for j in range(i + 1, len(trades)):
            next_time = datetime.fromisoformat(trades[j].entryAt.replace("Z", "+00:00"))

            if next_time - start_time <= timedelta(minutes=30):
                count += 1
            else:
                break

        if count > 10:
            overtrading = True
            break

    return {
        "totalTrades": total,
        "wins": wins,
        "planAdherenceScore": avg_adherence,
        "revengeTrades": revenge_count,
        "sessionTilt": session_tilt,
        "winRateByEmotion": emotion_winrate,
        "overtradingDetected": overtrading
    }