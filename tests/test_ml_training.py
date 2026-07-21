import pandas as pd
from sklearn.linear_model import LinearRegression

from app.ml.features import build_price_training_dataset
from app.ml.training import train_baseline_price_model


def test_train_baseline_price_model_returns_fitted_model_and_metrics():
    cleaned_df = pd.DataFrame(
        [
            {
                "estimate_low": 400.0,
                "estimate_high": 550.0,
                "size_ml": 700,
                "quantity": 1,
                "result_price": 450.0,
            },
            {
                "estimate_low": 70.0,
                "estimate_high": 110.0,
                "size_ml": 700,
                "quantity": 1,
                "result_price": 85.0,
            },
            {
                "estimate_low": 100.0,
                "estimate_high": 150.0,
                "size_ml": 700,
                "quantity": 1,
                "result_price": 120.0,
            },
            {
                "estimate_low": 180.0,
                "estimate_high": 240.0,
                "size_ml": 700,
                "quantity": 1,
                "result_price": 210.0,
            },
        ]
    )

    X, y = build_price_training_dataset(cleaned_df)

    model, metrics = train_baseline_price_model(X, y)

    assert isinstance(model, LinearRegression)

    assert "training_rows" in metrics
    assert "mae" in metrics
    assert "r2" in metrics

    assert metrics["training_rows"] == 4
    assert metrics["mae"] >= 0