from sqlalchemy import Column, String, Float, Integer
from app.database.db import Base

class Trade(Base):
    __tablename__ = "trades"

    tradeId = Column(String, primary_key=True, index=True)
    userId = Column(String)
    sessionId = Column(String)
    asset = Column(String)
    assetClass = Column(String)
    direction = Column(String)
    entryPrice = Column(Float)
    exitPrice = Column(Float)
    quantity = Column(Float)
    entryAt = Column(String)
    exitAt = Column(String)
    status = Column(String)
    planAdherence = Column(Integer)
    emotionalState = Column(String)
    entryRationale = Column(String)