from fastapi.testclient import TestClient
from app.main import app
from io import BytesIO


client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_sales_test_endpoint():
    response = client.get("/sales/test")

    assert response.status_code == 200

    response_body = response.json()

    assert response_body["message"] == "Sales routes are connected"
    assert response_body["next_step"] == "CSV upload endpoint"

def test_upload_valid_sample_csv():
    with open("data/sample/sample_auction_lots.csv", "rb") as csv_file:
        response = client.post(
            "/sales/upload",
            files={"file": ("sample_auction_lots.csv", csv_file, "text/csv")},
        )

    assert response.status_code == 200

    response_body = response.json()

    assert response_body["filename"] == "sample_auction_lots.csv"
    assert response_body["rows_received"] == 10
    assert response_body["columns_received"] == 16
    assert response_body["validation"]["is_valid"] is True
    assert response_body["validation"]["missing_columns"] == []
    assert "cleaned_preview" in response_body
    assert len(response_body["cleaned_preview"]) > 0

    first_cleaned_row = response_body["cleaned_preview"][0]

    assert "auction_date" in first_cleaned_row
    assert first_cleaned_row["auction_date"] == "2025-03-23"
    assert first_cleaned_row["size_ml"] == 700
    assert first_cleaned_row["quantity"] == 1
    assert first_cleaned_row["estimate_low"] == 400.0
    assert first_cleaned_row["estimate_high"] == 550.0
    assert first_cleaned_row["estimate_currency"] == "GBP"

def test_upload_rejects_non_csv_file():
    fake_file = BytesIO(b"this is not a proper csv file")

    response = client.post(
        "/sales/upload",
        files={"file": ("not_a_csv.txt", fake_file, "text/plain")},
    )

    assert response.status_code == 400
    response_body = response.json()
    assert response_body["detail"]["message"] == "Only CSV files are supported."

def test_upload_rejects_csv_with_missing_columns():
    bad_csv = BytesIO(
        b"Wrong_Column,Another_Wrong_Column\n"
        b"value1,value2\n"
    )

    response = client.post(
        "/sales/upload",
        files={"file": ("bad_file.csv", bad_csv, "text/csv")},
    )

    assert response.status_code == 400

    response_body = response.json()

    assert response_body["detail"]["message"] == "Uploaded CSV is missing required columns."
    assert "Auction_Name" in response_body["detail"]["missing_columns"]