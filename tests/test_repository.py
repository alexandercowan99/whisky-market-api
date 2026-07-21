from app.db.repository import build_auction_lot_from_row

def test_build_auction_lot_from_cleaned_row():
    row = {
        "Auction_Name": "Highland Whisky Auctions",
        "Auction_Title": "March 2025 Rare Whisky Sale",
        "Auction_Link": "https://example.com/auction/001",
        "Auction_Date_String": "Ended Mar 23 2025 at 11:00 PM",
        "auction_date": "2025-03-23",
        "Auction_Lot_Total": "150 Lots",
        "Lot_Link": "https://example.com/auction/001/lot/1",
        "Lot_Title": "Macallan 18 Year Old Sherry Oak",
        "Lot_Number": "Lot 1",
        "Lot_Category": "SINGLE MALT",
        "Lot_Result_String": "RESULT £450 SOLD",
        "result_price": 450.0,
        "result_currency": "GBP",
        "sale_status": "sold",
        "Lot_Estimate_String": "ESTIMATE £400-£550",
        "estimate_low": 400.0,
        "estimate_high": 550.0,
        "estimate_currency": "GBP",
        "size_ml": 700,
        "quantity": 1,
        "Lot_Details": "SIZE 700 ml QUANTITY 1 Bottle",
        "Lot_Condition": "Good condition",
        "Lot_Description": "Synthetic description for testing.",
    }

    auction_lot = build_auction_lot_from_row(row)

    assert auction_lot.auction_name == "Highland Whisky Auctions"
    assert auction_lot.auction_title == "March 2025 Rare Whisky Sale"
    assert auction_lot.auction_link == "https://example.com/auction/001"
    assert auction_lot.auction_date_raw == "Ended Mar 23 2025 at 11:00 PM"
    assert auction_lot.auction_date == "2025-03-23"
    assert auction_lot.auction_lot_total == "150 Lots"

    assert auction_lot.lot_link == "https://example.com/auction/001/lot/1"
    assert auction_lot.lot_title == "Macallan 18 Year Old Sherry Oak"
    assert auction_lot.lot_number == "Lot 1"
    assert auction_lot.lot_category == "SINGLE MALT"

    assert auction_lot.result_raw == "RESULT £450 SOLD"
    assert auction_lot.result_price == 450.0
    assert auction_lot.result_currency == "GBP"
    assert auction_lot.sale_status == "sold"

    assert auction_lot.estimate_raw == "ESTIMATE £400-£550"
    assert auction_lot.estimate_low == 400.0
    assert auction_lot.estimate_high == 550.0
    assert auction_lot.estimate_currency == "GBP"

    assert auction_lot.size_ml == 700
    assert auction_lot.quantity == 1

    assert auction_lot.lot_details == "SIZE 700 ml QUANTITY 1 Bottle"
    assert auction_lot.lot_condition == "Good condition"
    assert auction_lot.lot_description == "Synthetic description for testing."