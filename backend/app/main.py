from fastapi import FastAPI
from app.database.db import engine, Base
from app.models import trade
from app.services.seed import load_seed_data

app = FastAPI()

Base.metadata.create_all(bind=engine)
load_seed_data()

@app.get("/")
def root():
    return {"message": "Seed Loaded"}