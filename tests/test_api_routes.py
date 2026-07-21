from io import BytesIO

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.database import Base, get_db
from app.db.models import AuctionLot
from app.main import app

@pytest.fixture()
def test_db():
    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_engine,
    )

    Base.metadata.create_all(bind=test_engine)

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=test_engine)

@pytest.fixture()
def client(test_db):
    def override_get_db():
        yield test_db

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()

def test_health_endpoint(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_sales_test_endpoint(client):
    response = client.get("/sales/test")

    assert response.status_code == 200

    response_body = response.json()

    assert response_body["message"] == "Sales routes are connected"
    assert response_body["next_step"] == "CSV upload endpoint"

def test_upload_valid_sample_csv(client, test_db):

    with open("data/sample/sample_auction_lots.csv", "rb") as csv_file:
        response = client.post(
            "/sales/upload",
            files={"file": ("sample_auction_lots.csv", csv_file, "text/csv")},
        )

    assert response.status_code == 200

    response_body = response.json()

    assert response_body["filename"] == "sample_auction_lots.csv"
    assert response_body["rows_received"] == 10
    assert response_body["rows_inserted"] == 10

    saved_lots = test_db.query(AuctionLot).all()

    assert len(saved_lots) == 10
    assert saved_lots[0].lot_title == "Macallan 18 Year Old Sherry Oak"
    assert saved_lots[0].auction_date == "2025-03-23"
    assert saved_lots[0].result_price == 450.0

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

    assert "upload_summary" in response_body

    upload_summary = response_body["upload_summary"]

    assert upload_summary["total_rows"] == 10
    assert upload_summary["sold_lots"] == 10
    assert upload_summary["unsold_lots"] == 0
    assert upload_summary["rows_with_result_price"] == 10
    assert upload_summary["rows_with_auction_date"] == 10
    assert upload_summary["average_result_price"] is not None

def test_upload_rejects_non_csv_file(client):
    fake_file = BytesIO(b"this is not a proper csv file")

    response = client.post(
        "/sales/upload",
        files={"file": ("not_a_csv.txt", fake_file, "text/plain")},
    )

    assert response.status_code == 400
    response_body = response.json()
    assert response_body["detail"]["message"] == "Only CSV files are supported."

def test_upload_rejects_csv_with_missing_columns(client):
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

def test_get_sales_lots_returns_saved_lots(client):
    with open("data/sample/sample_auction_lots.csv", "rb") as csv_file:
        upload_response = client.post(
            "/sales/upload",
            files={"file": ("sample_auction_lots.csv", csv_file, "text/csv")},
        )

    assert upload_response.status_code == 200

    response = client.get("/sales/lots")

    assert response.status_code == 200

    response_body = response.json()

    assert response_body["count"] == 10
    assert len(response_body["lots"]) == 10

    first_lot = response_body["lots"][0]

    assert first_lot["lot_title"] == "Macallan 18 Year Old Sherry Oak"
    assert first_lot["auction_name"] == "Highland Whisky Auctions"
    assert first_lot["auction_date"] == "2025-03-23"
    assert first_lot["result_price"] == 450.0

def test_get_sales_lots_accepts_limit_parameter(client):
    with open("data/sample/sample_auction_lots.csv", "rb") as csv_file:
        upload_response = client.post(
            "/sales/upload",
            files={"file": ("sample_auction_lots.csv", csv_file, "text/csv")},
        )

    assert upload_response.status_code == 200

    response = client.get("/sales/lots?limit=3")

    assert response.status_code == 200

    response_body = response.json()

    assert response_body["count"] == 3
    assert len(response_body["lots"]) == 3

def test_get_sales_lots_accepts_sale_status_filter(client):
    with open("data/sample/sample_auction_lots.csv", "rb") as csv_file:
        upload_response = client.post(
            "/sales/upload",
            files={"file": ("sample_auction_lots.csv", csv_file, "text/csv")},
        )

    assert upload_response.status_code == 200

    sold_response = client.get("/sales/lots?sale_status=sold")

    assert sold_response.status_code == 200

    sold_response_body = sold_response.json()

    assert sold_response_body["count"] == 10
    assert len(sold_response_body["lots"]) == 10

    for lot in sold_response_body["lots"]:
        assert lot["sale_status"] == "sold"

    unsold_response = client.get("/sales/lots?sale_status=unsold")

    assert unsold_response.status_code == 200

    unsold_response_body = unsold_response.json()

    assert unsold_response_body["count"] == 0
    assert unsold_response_body["lots"] == []

def test_get_sales_lots_rejects_invalid_limit(client):
    response = client.get("/sales/lots?limit=0")

    assert response.status_code == 422


def test_get_sales_lots_rejects_invalid_sale_status(client):
    response = client.get("/sales/lots?sale_status=random")

    assert response.status_code == 422

def test_get_sales_summary_returns_database_summary(client):
    with open("data/sample/sample_auction_lots.csv", "rb") as csv_file:
        upload_response = client.post(
            "/sales/upload",
            files={"file": ("sample_auction_lots.csv", csv_file, "text/csv")},
        )

    assert upload_response.status_code == 200

    response = client.get("/sales/summary")

    assert response.status_code == 200

    response_body = response.json()

    assert response_body["total_lots"] == 10
    assert response_body["sold_lots"] == 10
    assert response_body["unsold_lots"] == 0
    assert response_body["rows_with_result_price"] == 10
    assert response_body["rows_with_auction_date"] == 10
    assert response_body["average_result_price"] is not None

def test_get_top_sales_lots_returns_highest_result_prices(client):
    with open("data/sample/sample_auction_lots.csv", "rb") as csv_file:
        upload_response = client.post(
            "/sales/upload",
            files={"file": ("sample_auction_lots.csv", csv_file, "text/csv")},
        )

    assert upload_response.status_code == 200

    response = client.get("/sales/top-lots?limit=3")

    assert response.status_code == 200

    response_body = response.json()

    assert response_body["count"] == 3
    assert len(response_body["lots"]) == 3

    result_prices = [
        lot["result_price"]
        for lot in response_body["lots"]
    ]

    assert result_prices == sorted(result_prices, reverse=True)
    assert all(price is not None for price in result_prices)

def test_get_auction_house_summary_returns_grouped_results(client):
    with open("data/sample/sample_auction_lots.csv", "rb") as csv_file:
        upload_response = client.post(
            "/sales/upload",
            files={"file": ("sample_auction_lots.csv", csv_file, "text/csv")},
        )

    assert upload_response.status_code == 200

    response = client.get("/sales/auction-houses")

    assert response.status_code == 200

    response_body = response.json()

    assert response_body["count"] == 5
    assert len(response_body["auction_houses"]) == 5

    highland_summary = next(
        auction_house
        for auction_house in response_body["auction_houses"]
        if auction_house["auction_name"] == "Highland Whisky Auctions"
    )

    assert highland_summary["total_lots"] == 2
    assert highland_summary["sold_lots"] == 2
    assert highland_summary["rows_with_result_price"] == 2
    assert highland_summary["average_result_price"] == 317.5

def test_get_sales_lots_accepts_auction_name_filter(client):
    with open("data/sample/sample_auction_lots.csv", "rb") as csv_file:
        upload_response = client.post(
            "/sales/upload",
            files={"file": ("sample_auction_lots.csv", csv_file, "text/csv")},
        )

    assert upload_response.status_code == 200

    response = client.get("/sales/lots?auction_name=Highland Whisky Auctions")

    assert response.status_code == 200

    response_body = response.json()

    assert response_body["count"] == 2
    assert len(response_body["lots"]) == 2

    for lot in response_body["lots"]:
        assert lot["auction_name"] == "Highland Whisky Auctions"

def test_get_monthly_sales_summary_returns_grouped_results(client):
    with open("data/sample/sample_auction_lots.csv", "rb") as csv_file:
        upload_response = client.post(
            "/sales/upload",
            files={"file": ("sample_auction_lots.csv", csv_file, "text/csv")},
        )

    assert upload_response.status_code == 200

    response = client.get("/sales/monthly-summary")

    assert response.status_code == 200

    response_body = response.json()

    assert response_body["count"] == 10
    assert len(response_body["monthly_summary"]) == 10

    march_summary = next(
        month
        for month in response_body["monthly_summary"]
        if month["auction_month"] == "2025-03"
    )

    assert march_summary["total_lots"] == 1
    assert march_summary["sold_lots"] == 1
    assert march_summary["rows_with_result_price"] == 1
    assert march_summary["average_result_price"] == 450.0