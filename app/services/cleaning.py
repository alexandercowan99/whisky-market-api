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

def parse_lot_details(details_string: str) -> dict:

    if not isinstance(details_string, str) or details_string.strip() == "":
        return {
            "size_ml": None,
            "quantity": None,
        }

    cleaned_text = details_string.upper().replace("\n", " ").strip()

    size_match = re.search(r"SIZE\s+(\d+)\s*ML", cleaned_text)
    quantity_match = re.search(r"QUANTITY\s+(\d+)", cleaned_text)

    size_ml = int(size_match.group(1)) if size_match else None
    quantity = int(quantity_match.group(1)) if quantity_match else None

    return {
        "size_ml": size_ml,
        "quantity": quantity,
    }

def parse_estimate_string(estimate_string: str) -> dict:

    if not isinstance(estimate_string, str) or estimate_string.strip() == "":
        return {
            "estimate_low": None,
            "estimate_high": None,
            "estimate_currency": None,
        }

    cleaned_text = estimate_string.upper().replace("\n", " ").strip()

    estimate_currency = None

    if "£" in cleaned_text:
        estimate_currency = "GBP"
    elif "$" in cleaned_text:
        estimate_currency = "USD"
    elif "€" in cleaned_text:
        estimate_currency = "EUR"

    estimate_match = re.search(
        r"[£$€]?\s?([\d,]+(?:\.\d+)?)\s*-\s*[£$€]?\s?([\d,]+(?:\.\d+)?)",
        cleaned_text,
    )

    if not estimate_match:
        return {
            "estimate_low": None,
            "estimate_high": None,
            "estimate_currency": estimate_currency,
        }

    estimate_low = float(estimate_match.group(1).replace(",", ""))
    estimate_high = float(estimate_match.group(2).replace(",", ""))

    return {
        "estimate_low": estimate_low,
        "estimate_high": estimate_high,
        "estimate_currency": estimate_currency,
    }

def add_cleaned_columns(df):
    df = df.copy()

    parsed_results = df["Lot_Result_String"].apply(parse_lot_result_string)

    df["result_price"] = parsed_results.apply(lambda result: result["result_price"])
    df["result_currency"] = parsed_results.apply(lambda result: result["currency"])
    df["sale_status"] = parsed_results.apply(lambda result: result["sale_status"])

    df["auction_date"] = df["Auction_Date_String"].apply(parse_auction_date_string)

    parsed_details = df["Lot_Details"].apply(parse_lot_details)

    df["size_ml"] = parsed_details.apply(lambda result: result["size_ml"])
    df["quantity"] = parsed_details.apply(lambda result: result["quantity"])

    parsed_estimates = df["Lot_Estimate_String"].apply(parse_estimate_string)

    df["estimate_low"] = parsed_estimates.apply(lambda result: result["estimate_low"])
    df["estimate_high"] = parsed_estimates.apply(lambda result: result["estimate_high"])
    df["estimate_currency"] = parsed_estimates.apply(lambda result: result["estimate_currency"])

    return df