import pandas as pd
import pytest

from app.ml.features import (
    NUMERIC_PRICE_FEATURE_COLUMNS,
    build_price_training_dataset,
)

def test_build_price_training_dataset_returns_features_and_target():
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
        ]
    )

    X, y = build_price_training_dataset(cleaned_df)

    assert list(X.columns) == NUMERIC_PRICE_FEATURE_COLUMNS
    assert len(X) == 2
    assert len(y) == 2

    assert X.iloc[0]["estimate_low"] == 400.0
    assert X.iloc[0]["estimate_high"] == 550.0
    assert y.tolist() == [450.0, 85.0]


def test_build_price_training_dataset_drops_rows_with_missing_values():
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
                "estimate_low": None,
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
                "result_price": None,
            },
        ]
    )

    X, y = build_price_training_dataset(cleaned_df)

    assert len(X) == 1
    assert len(y) == 1
    assert y.tolist() == [450.0]


def test_build_price_training_dataset_raises_error_for_missing_columns():
    cleaned_df = pd.DataFrame(
        [
            {
                "estimate_low": 400.0,
                "estimate_high": 550.0,
                "result_price": 450.0,
            }
        ]
    )

    with pytest.raises(ValueError, match="Missing required columns"):
        build_price_training_dataset(cleaned_df)