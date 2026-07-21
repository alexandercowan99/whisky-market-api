import pandas as pd
from sqlalchemy.orm import Session
from app.db.models import AuctionLot

def build_auction_lot_from_row(row) -> AuctionLot:

    return AuctionLot(
        auction_name=row.get("Auction_Name"),
        auction_title=row.get("Auction_Title"),
        auction_link=row.get("Auction_Link"),
        auction_date_raw=row.get("Auction_Date_String"),
        auction_date=row.get("auction_date"),
        auction_lot_total=row.get("Auction_Lot_Total"),
        lot_link=row.get("Lot_Link"),
        lot_title=row.get("Lot_Title"),
        lot_number=row.get("Lot_Number"),
        lot_category=row.get("Lot_Category"),
        result_raw=row.get("Lot_Result_String"),
        result_price=row.get("result_price"),
        result_currency=row.get("result_currency"),
        sale_status=row.get("sale_status"),
        estimate_raw=row.get("Lot_Estimate_String"),
        estimate_low=row.get("estimate_low"),
        estimate_high=row.get("estimate_high"),
        estimate_currency=row.get("estimate_currency"),
        size_ml=row.get("size_ml"),
        quantity=row.get("quantity"),
        lot_details=row.get("Lot_Details"),
        lot_condition=row.get("Lot_Condition"),
        lot_description=row.get("Lot_Description"),
    )

def insert_auction_lots(db: Session, cleaned_df: pd.DataFrame) -> int:
    auction_lots = []

    for _, row in cleaned_df.iterrows():
        auction_lot = build_auction_lot_from_row(row)
        auction_lots.append(auction_lot)

    db.add_all(auction_lots)
    db.commit()

    return len(auction_lots)

def get_auction_lots(db: Session, limit: int = 100) -> list[AuctionLot]:
    return db.query(AuctionLot).limit(limit).all()