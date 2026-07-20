from sqlalchemy import Column, Float, Integer, String, Text

from app.db.database import Base

class AuctionLot(Base):
    __tablename__ = "auction_lots"

    id = Column(Integer, primary_key=True, index=True)

    auction_name = Column(String, nullable=False)
    auction_title = Column(String, nullable=True)
    auction_link = Column(String, nullable=True)
    auction_date_raw = Column(String, nullable=True)
    auction_date = Column(String, nullable=True)
    auction_lot_total = Column(String, nullable=True)

    lot_link = Column(String, nullable=True)
    lot_title = Column(String, nullable=False)
    lot_number = Column(String, nullable=True)
    lot_category = Column(String, nullable=True)

    result_raw = Column(String, nullable=True)
    result_price = Column(Float, nullable=True)
    result_currency = Column(String, nullable=True)
    sale_status = Column(String, nullable=True)

    estimate_raw = Column(String, nullable=True)
    estimate_low = Column(Float, nullable=True)
    estimate_high = Column(Float, nullable=True)
    estimate_currency = Column(String, nullable=True)

    size_ml = Column(Integer, nullable=True)
    quantity = Column(Integer, nullable=True)

    lot_details = Column(Text, nullable=True)
    lot_condition = Column(Text, nullable=True)
    lot_description = Column(Text, nullable=True)