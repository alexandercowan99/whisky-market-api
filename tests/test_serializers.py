from app.api.serializers import serialize_auction_lot
from app.db.models import AuctionLot

def test_serialize_auction_lot_returns_response_dictionary():
    lot = AuctionLot(
        id=1,
        auction_name="Highland Whisky Auctions",
        auction_date="2025-03-23",
        lot_title="Macallan 18 Year Old Sherry Oak",
        lot_category="SINGLE MALT",
        result_price=450.0,
        result_currency="GBP",
        sale_status="sold",
        estimate_low=400.0,
        estimate_high=550.0,
        estimate_currency="GBP",
        size_ml=700,
        quantity=1,
    )

    result = serialize_auction_lot(lot)

    assert result == {
        "id": 1,
        "auction_name": "Highland Whisky Auctions",
        "auction_date": "2025-03-23",
        "lot_title": "Macallan 18 Year Old Sherry Oak",
        "lot_category": "SINGLE MALT",
        "result_price": 450.0,
        "result_currency": "GBP",
        "sale_status": "sold",
        "estimate_low": 400.0,
        "estimate_high": 550.0,
        "estimate_currency": "GBP",
        "size_ml": 700,
        "quantity": 1,
    }