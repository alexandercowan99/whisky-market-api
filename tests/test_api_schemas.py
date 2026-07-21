import pytest
from pydantic import ValidationError

from app.api.schemas import (
    PricePredictionRequest,
    PricePredictionResponse,
)

def test_price_prediction_request_accepts_valid_input():
    request = PricePredictionRequest(
        estimate_low=400.0,
        estimate_high=550.0,
        size_ml=700,
        quantity=1,
    )

    assert request.estimate_low == 400.0
    assert request.estimate_high == 550.0
    assert request.size_ml == 700
    assert request.quantity == 1

def test_price_prediction_request_rejects_missing_fields():
    with pytest.raises(ValidationError):
        PricePredictionRequest(
            estimate_low=400.0,
            estimate_high=550.0,
        )

def test_price_prediction_request_rejects_negative_values():
    with pytest.raises(ValidationError):
        PricePredictionRequest(
            estimate_low=-400.0,
            estimate_high=550.0,
            size_ml=700,
            quantity=1,
        )

def test_price_prediction_response_schema():
    response = PricePredictionResponse(
        predicted_price=450.25,
        model_version="baseline-linear-regression-v1",
    )

    assert response.predicted_price == 450.25
    assert response.model_version == "baseline-linear-regression-v1"
