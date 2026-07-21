from pydantic import BaseModel, Field

class AuctionLotResponse(BaseModel):
    id: int
    auction_name: str | None
    auction_date: str | None
    lot_title: str | None
    lot_category: str | None
    result_price: float | None
    result_currency: str | None
    sale_status: str | None
    estimate_low: float | None
    estimate_high: float | None
    estimate_currency: str | None
    size_ml: int | None
    quantity: int | None

class AuctionLotsResponse(BaseModel):
    count: int
    lots: list[AuctionLotResponse]

class PricePredictionRequest(BaseModel):
    estimate_low: float = Field(ge=0)
    estimate_high: float = Field(ge=0)
    size_ml: int = Field(ge=1)
    quantity: int = Field(ge=1)

class PricePredictionResponse(BaseModel):
    predicted_price: float
    model_version: str