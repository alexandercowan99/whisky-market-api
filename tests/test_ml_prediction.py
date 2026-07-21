import pandas as pd
import pytest
from sklearn.linear_model import LinearRegression

from app.ml.model_io import save_model
from app.ml.prediction import predict_price, predict_price_from_model_file


def test_predict_price_returns_float_prediction():
    X = pd.DataFrame(
        {
            "estimate_low": [400.0, 70.0, 100.0],
            "estimate_high": [550.0, 110.0, 150.0],
            "size_ml": [700, 700, 700],
            "quantity": [1, 1, 1],
        }
    )

    y = pd.Series([450.0, 85.0, 120.0])

    model = LinearRegression()
    model.fit(X, y)

    input_features = {
        "estimate_low": 400.0,
        "estimate_high": 550.0,
        "size_ml": 700,
        "quantity": 1,
    }

    prediction = predict_price(model, input_features)

    assert isinstance(prediction, float)
    assert prediction > 0


def test_predict_price_raises_error_for_missing_features():
    model = LinearRegression()

    input_features = {
        "estimate_low": 400.0,
        "estimate_high": 550.0,
    }

    with pytest.raises(ValueError, match="Missing required prediction features"):
        predict_price(model, input_features)


def test_predict_price_from_model_file_loads_model_and_predicts(tmp_path):
    X = pd.DataFrame(
        {
            "estimate_low": [400.0, 70.0, 100.0],
            "estimate_high": [550.0, 110.0, 150.0],
            "size_ml": [700, 700, 700],
            "quantity": [1, 1, 1],
        }
    )

    y = pd.Series([450.0, 85.0, 120.0])

    model = LinearRegression()
    model.fit(X, y)

    model_path = tmp_path / "price_model.joblib"
    save_model(model, model_path)

    input_features = {
        "estimate_low": 400.0,
        "estimate_high": 550.0,
        "size_ml": 700,
        "quantity": 1,
    }

    prediction = predict_price_from_model_file(model_path, input_features)

    assert isinstance(prediction, float)
    assert prediction > 0