from sqlalchemy.orm import Session
from app.database.db import SessionLocal
from app.models.trade import Trade
from datetime import datetime, timedelta
from collections import defaultdict

def process_metrics(userId: str):
    db: Session = SessionLocal()

    trades = db.query(Trade).filter(Trade.userId == userId).all()
    trades = sorted(trades, key=lambda x: x.entryAt)

    total = len(trades)

    wins = 0
    for t in trades:
        if t.exitPrice and t.entryPrice and t.exitPrice > t.entryPrice:
            wins += 1

    last_10 = trades[-10:]
    adherence_values = [t.planAdherence for t in last_10 if t.planAdherence is not None]

    avg_adherence = sum(adherence_values) / len(adherence_values) if adherence_values else 0

    revenge_count = 0

    for i in range(1, len(trades)):
        prev = trades[i - 1]
        curr = trades[i]

        if prev.exitPrice and prev.entryPrice and prev.exitPrice < prev.entryPrice:
            prev_time = datetime.fromisoformat(prev.exitAt.replace("Z", "+00:00"))
            curr_time = datetime.fromisoformat(curr.entryAt.replace("Z", "+00:00"))

            if (curr_time - prev_time).total_seconds() <= 90 and curr.emotionalState in ["anxious", "fearful"]:
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
        session_tilt[session_id] = loss_following / total_session_trades if total_session_trades else 0

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
        emotion_winrate[emotion] = wins_e / total_e if total_e else 0

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

    db.close()