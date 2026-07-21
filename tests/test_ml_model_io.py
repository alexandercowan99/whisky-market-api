import pandas as pd
import pytest
from sklearn.linear_model import LinearRegression

from app.ml.model_io import load_model, save_model


def test_save_and_load_model_round_trip(tmp_path):
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

    assert model_path.exists()

    loaded_model = load_model(model_path)

    original_predictions = model.predict(X)
    loaded_predictions = loaded_model.predict(X)

    assert isinstance(loaded_model, LinearRegression)
    assert loaded_predictions.tolist() == pytest.approx(
        original_predictions.tolist()
    )