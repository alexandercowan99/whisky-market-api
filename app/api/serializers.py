from app.db.models import AuctionLot

def serialize_auction_lot(lot: AuctionLot) -> dict:
    return {
        "id": lot.id,
        "auction_name": lot.auction_name,
        "auction_date": lot.auction_date,
        "lot_title": lot.lot_title,
        "lot_category": lot.lot_category,
        "result_price": lot.result_price,
        "result_currency": lot.result_currency,
        "sale_status": lot.sale_status,
        "estimate_low": lot.estimate_low,
        "estimate_high": lot.estimate_high,
        "estimate_currency": lot.estimate_currency,
        "size_ml": lot.size_ml,
        "quantity": lot.quantity,
    }
