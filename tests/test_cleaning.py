from app.services.cleaning import parse_auction_date_string, parse_lot_result_string, parse_lot_details, parse_estimate_string

def test_parse_gbp_sold_result():
    result = parse_lot_result_string("RESULT £450 SOLD")

    assert result["result_price"] == 450.0
    assert result["currency"] == "GBP"
    assert result["sale_status"] == "sold"


def test_parse_usd_sold_result_with_commas_and_new_lines():
    result = parse_lot_result_string("RESULT\n$18,000\nSOLD")

    assert result["result_price"] == 18000.0
    assert result["currency"] == "USD"
    assert result["sale_status"] == "sold"


def test_parse_unsold_result():
    result = parse_lot_result_string("RESULT UNSOLD")

    assert result["result_price"] is None
    assert result["currency"] is None
    assert result["sale_status"] == "unsold"


def test_parse_empty_result():
    result = parse_lot_result_string("")

    assert result["result_price"] is None
    assert result["currency"] is None
    assert result["sale_status"] == "unknown"


def test_parse_none_result():
    result = parse_lot_result_string(None)

    assert result["result_price"] is None
    assert result["currency"] is None
    assert result["sale_status"] == "unknown"

def test_parse_auction_date_string():
    result = parse_auction_date_string("Ended Mar 23 2025 at 11:00 PM")

    assert result == "2025-03-23"

def test_parse_auction_date_string_without_ended_prefix():
    result = parse_auction_date_string("Apr 12 2025 at 9:00 PM")

    assert result == "2025-04-12"


def test_parse_empty_auction_date_string():
    result = parse_auction_date_string("")

    assert result is None


def test_parse_invalid_auction_date_string():
    result = parse_auction_date_string("not a real date")

    assert result is None

def test_parse_lot_details_size_and_quantity():
    result = parse_lot_details("SIZE 700 ml QUANTITY 1 Bottle")

    assert result["size_ml"] == 700
    assert result["quantity"] == 1


def test_parse_lot_details_multiline():
    result = parse_lot_details("SIZE\n750 ml\nQUANTITY\n2 Bottles")

    assert result["size_ml"] == 750
    assert result["quantity"] == 2


def test_parse_empty_lot_details():
    result = parse_lot_details("")

    assert result["size_ml"] is None
    assert result["quantity"] is None

def test_parse_gbp_estimate_string():
    result = parse_estimate_string("ESTIMATE £400-£550")

    assert result["estimate_low"] == 400.0
    assert result["estimate_high"] == 550.0
    assert result["estimate_currency"] == "GBP"


def test_parse_usd_estimate_string_with_commas():
    result = parse_estimate_string("ESTIMATE $17,500-$22,000")

    assert result["estimate_low"] == 17500.0
    assert result["estimate_high"] == 22000.0
    assert result["estimate_currency"] == "USD"


def test_parse_empty_estimate_string():
    result = parse_estimate_string("")

    assert result["estimate_low"] is None
    assert result["estimate_high"] is None
    assert result["estimate_currency"] is None


def test_parse_invalid_estimate_string():
    result = parse_estimate_string("No estimate available")

    assert result["estimate_low"] is None
    assert result["estimate_high"] is None
    assert result["estimate_currency"] is None