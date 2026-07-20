from app.services.cleaning import parse_lot_result_string

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