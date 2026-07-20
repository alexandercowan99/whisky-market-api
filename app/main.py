from fastapi import FastAPI
from app.api import routes_health

app = FastAPI(
    title="Whisky Market Data API",
    description="API for uploading, validating and analysing whisky market data.",
    version="0.1.0"
)

app.include_router(routes_health.router)