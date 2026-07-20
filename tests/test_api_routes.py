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