from fastapi import FastAPI
from app.database.db import engine, Base
from app.models import trade
from app.services.seed import load_seed_data
from app.routes import user
from app.routes import trade
from app.routes import metrics
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(trade.router)
app.include_router(metrics.router)

Base.metadata.create_all(bind=engine)
load_seed_data()

@app.get("/")
def root():
    return {"message": "Seed Loaded"}