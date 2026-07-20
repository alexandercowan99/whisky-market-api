import re
from datetime import datetime

def parse_lot_result_string(result_string: str) -> dict:
    """
    Parse a raw auction lot result string into structured fields.

    Example inputs:
    - "RESULT £450 SOLD"
    - "RESULT\n$18,000\nSOLD"
    - "RESULT UNSOLD"
    """

    if not isinstance(result_string, str) or result_string.strip() == "":
        return {
            "result_price": None,
            "currency": None,
            "sale_status": "unknown",
        }

    cleaned_text = result_string.upper().replace("\n", " ").strip()

    if "UNSOLD" in cleaned_text:
        sale_status = "unsold"
    elif "SOLD" in cleaned_text:
        sale_status = "sold"
    else:
        sale_status = "unknown"

    currency = None

    if "£" in cleaned_text:
        currency = "GBP"
    elif "$" in cleaned_text:
        currency = "USD"
    elif "€" in cleaned_text:
        currency = "EUR"

    price_match = re.search(r"[£$€]?\s?([\d,]+(?:\.\d+)?)", cleaned_text)

    if price_match:
        price_text = price_match.group(1).replace(",", "")
        result_price = float(price_text)
    else:
        result_price = None

    return {
        "result_price": result_price,
        "currency": currency,
        "sale_status": sale_status,
    }

def add_cleaned_columns(df):
    df = df.copy()

    parsed_results = df["Lot_Result_String"].apply(parse_lot_result_string)

    df["result_price"] = parsed_results.apply(lambda result: result["result_price"])
    df["result_currency"] = parsed_results.apply(lambda result: result["currency"])
    df["sale_status"] = parsed_results.apply(lambda result: result["sale_status"])

    df["auction_date"] = df["Auction_Date_String"].apply(parse_auction_date_string)

    return df

def parse_auction_date_string(date_string: str) -> str | None:

    if not isinstance(date_string, str) or date_string.strip() == "":
        return None

    cleaned_text = date_string.strip()

    if cleaned_text.lower().startswith("ended "):
        cleaned_text = cleaned_text[6:]

    try:
        parsed_datetime = datetime.strptime(cleaned_text, "%b %d %Y at %I:%M %p")
    except ValueError:
        return None

    return parsed_datetime.date().isoformat()