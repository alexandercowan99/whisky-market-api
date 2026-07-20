from fastapi.testclient import TestClient

from app.main import app

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