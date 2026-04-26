import json
from app.database.db import SessionLocal
from app.models.trade import Trade

def load_seed_data():
    db = SessionLocal()

    if db.query(Trade).first():
        db.close()
        return

    with open("app/data/nevup_seed_dataset.json") as f:
        data = json.load(f)

    for trader in data["traders"]:
        for session in trader["sessions"]:
            for t in session["trades"]:
                trade = Trade(
                    tradeId=t.get("tradeId"),
                    userId=t.get("userId"),
                    sessionId=t.get("sessionId"),
                    asset=t.get("asset"),
                    assetClass=t.get("assetClass"),
                    direction=t.get("direction"),
                    entryPrice=t.get("entryPrice"),
                    exitPrice=t.get("exitPrice"),
                    quantity=t.get("quantity"),
                    entryAt=t.get("entryAt"),
                    exitAt=t.get("exitAt"),
                    status=t.get("status"),
                    planAdherence=t.get("planAdherence"),
                    emotionalState=t.get("emotionalState"),
                    entryRationale=t.get("entryRationale"),
                )
                db.add(trade)

    db.commit()
    db.close()