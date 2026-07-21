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

def get_auction_lots(db: Session, limit: int = 100, sale_status: str | None = None, 
                     auction_name: str | None = None, min_price: float | None = None,
                     max_price: float | None = None,) -> list[AuctionLot]:

    query = db.query(AuctionLot)

    if sale_status is not None:
        query = query.filter(AuctionLot.sale_status == sale_status)
    
    if auction_name is not None:
        query = query.filter(AuctionLot.auction_name == auction_name)

    if min_price is not None:
        query = query.filter(AuctionLot.result_price >= min_price)

    if max_price is not None:
        query = query.filter(AuctionLot.result_price <= max_price)

    return query.limit(limit).all()

def get_sales_summary(db: Session) -> dict:

    lots = db.query(AuctionLot).all()

    sold_lots = sum(1 for lot in lots if lot.sale_status == "sold")
    unsold_lots = sum(1 for lot in lots if lot.sale_status == "unsold")

    result_prices = [
        lot.result_price
        for lot in lots
        if lot.result_price is not None
    ]

    rows_with_result_price = len(result_prices)

    rows_with_auction_date = sum(
        1 for lot in lots
        if lot.auction_date is not None
    )

    average_result_price = (
        round(sum(result_prices) / len(result_prices), 2)
        if result_prices
        else None
    )

    return {
        "total_lots": len(lots),
        "sold_lots": sold_lots,
        "unsold_lots": unsold_lots,
        "rows_with_result_price": rows_with_result_price,
        "rows_with_auction_date": rows_with_auction_date,
        "average_result_price": average_result_price,
    }

def get_top_auction_lots(db: Session, limit: int = 10) -> dict:

    return db.query(AuctionLot).filter(AuctionLot.result_price.isnot(None)).order_by(AuctionLot.result_price.desc()).limit(limit).all()

def get_auction_house_summary(db: Session) -> list[dict]:
    lots = db.query(AuctionLot).all()

    summary_by_house = {}

    for lot in lots:
        auction_name = lot.auction_name or "Unknown"

        if auction_name not in summary_by_house:
            summary_by_house[auction_name] = {
                "auction_name": auction_name,
                "total_lots": 0,
                "sold_lots": 0,
                "result_prices": [],
            }

        summary_by_house[auction_name]["total_lots"] += 1

        if lot.sale_status == "sold":
            summary_by_house[auction_name]["sold_lots"] += 1   

        if lot.result_price is not None:
            summary_by_house[auction_name]["result_prices"].append(lot.result_price)

    auction_house_summaries = []

    for auction_house in summary_by_house.values():
        result_prices = auction_house["result_prices"]

        average_result_price = (
            round(sum(result_prices) / len(result_prices), 2)
            if result_prices
            else None
        )

        auction_house_summaries.append(
            {
                "auction_name": auction_house["auction_name"],
                "total_lots": auction_house["total_lots"],
                "sold_lots": auction_house["sold_lots"],
                "rows_with_result_price": len(result_prices),
                "average_result_price": average_result_price,
            }
        )

    return auction_house_summaries

def get_monthly_sales_summary(db: Session) -> list[dict]:

    lots = db.query(AuctionLot).all()

    summary_by_month = {}

    for lot in lots:
        auction_month = lot.auction_date[:7] if lot.auction_date else "Unknown"

        if auction_month not in summary_by_month:
            summary_by_month[auction_month] = {
                "auction_month": auction_month,
                "total_lots": 0,
                "sold_lots": 0,
                "result_prices": [],
            }

        summary_by_month[auction_month]["total_lots"] += 1

        if lot.sale_status == "sold":
            summary_by_month[auction_month]["sold_lots"] += 1

        if lot.result_price is not None:
            summary_by_month[auction_month]["result_prices"].append(lot.result_price)

    monthly_summaries = []

    for month_summary in summary_by_month.values():
        result_prices = month_summary["result_prices"]

        average_result_price = (
            round(sum(result_prices) / len(result_prices), 2)
            if result_prices
            else None
        )

        monthly_summaries.append(
            {
                "auction_month": month_summary["auction_month"],
                "total_lots": month_summary["total_lots"],
                "sold_lots": month_summary["sold_lots"],
                "rows_with_result_price": len(result_prices),
                "average_result_price": average_result_price,
            }
        )

    return sorted(
        monthly_summaries,
        key=lambda month_summary: month_summary["auction_month"],
    )

