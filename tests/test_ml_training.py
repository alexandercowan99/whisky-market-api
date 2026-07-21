import pandas as pd
from sklearn.linear_model import LinearRegression

from app.ml.features import build_price_training_dataset
from app.ml.training import train_baseline_price_model, train_evaluate_baseline_price_model, train_and_save_price_model


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

def test_train_evaluate_baseline_price_model_uses_train_test_split():
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
            {
                "estimate_low": 140.0,
                "estimate_high": 190.0,
                "size_ml": 700,
                "quantity": 1,
                "result_price": 165.0,
            },
            {
                "estimate_low": 90.0,
                "estimate_high": 130.0,
                "size_ml": 700,
                "quantity": 1,
                "result_price": 115.0,
            },
        ]
    )

    X, y = build_price_training_dataset(cleaned_df)

    model, metrics = train_evaluate_baseline_price_model(
        X,
        y,
        test_size=0.33,
        random_state=42,
    )

    assert isinstance(model, LinearRegression)

    assert metrics["training_rows"] == 4
    assert metrics["test_rows"] == 2

    assert "train_mae" in metrics
    assert "test_mae" in metrics
    assert "test_r2" in metrics

    assert metrics["train_mae"] >= 0
    assert metrics["test_mae"] >= 0

def test_train_and_save_price_model_creates_model_file(tmp_path):
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
            {
                "estimate_low": 140.0,
                "estimate_high": 190.0,
                "size_ml": 700,
                "quantity": 1,
                "result_price": 165.0,
            },
            {
                "estimate_low": 90.0,
                "estimate_high": 130.0,
                "size_ml": 700,
                "quantity": 1,
                "result_price": 115.0,
            },
        ]
    )

    model_path = tmp_path / "price_model.joblib"

    metrics = train_and_save_price_model(
        cleaned_df=cleaned_df,
        model_path=model_path,
        test_size=0.33,
        random_state=42,
    )

    assert model_path.exists()

    assert metrics["training_rows"] == 4
    assert metrics["test_rows"] == 2
    assert metrics["model_path"] == str(model_path)
    assert "train_mae" in metrics
    assert "test_mae" in metrics
    assert "test_r2" in metrics