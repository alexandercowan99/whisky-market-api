REQUIRED_AUCTION_LOT_COLUMNS = [
    "Auction_Name",
    "Auction_Title",
    "Auction_Link",
    "Auction_Date_String",
    "Auction_Lot_Total",
    "Lot_Link",
    "Lot_Title",
    "Total_Lots_Scraped",
    "Lot_Number",
    "Lot_Category",
    "Lot_Result_String",
    "Lot_Estimate_String",
    "Lot_Reserve_String",
    "Lot_Details",
    "Lot_Condition",
    "Lot_Description",
]


def validate_required_columns(received_columns: list[str]) -> dict:
    missing_columns = [
        column for column in REQUIRED_AUCTION_LOT_COLUMNS
        if column not in received_columns
    ]

    extra_columns = [
        column for column in received_columns
        if column not in REQUIRED_AUCTION_LOT_COLUMNS
    ]

    return {
        "is_valid": len(missing_columns) == 0,
        "missing_columns": missing_columns,
        "extra_columns": extra_columns,
    }