from fastapi import FastAPI

from app.api import routes_health, routes_sales
from app.db import models
from app.db.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Whisky Market Data API",
    description="API for uploading, validating and analysing whisky market data.",
    version="0.1.0",
)

app.include_router(routes_health.router)
app.include_router(routes_sales.router)