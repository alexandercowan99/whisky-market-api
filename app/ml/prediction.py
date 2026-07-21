from pathlib import Path
from typing import Any

import pandas as pd

from app.ml.features import NUMERIC_PRICE_FEATURE_COLUMNS
from app.ml.model_io import load_model


def predict_price(model: Any, input_features: dict) -> float:

    missing_features = [
    column for column in NUMERIC_PRICE_FEATURE_COLUMNS
    if column not in input_features
    ]

    if missing_features:
        raise ValueError(
            f"Missing required prediction features: {missing_features}"
        )
    
    input_df = pd.DataFrame([input_features])
    input_df = input_df[NUMERIC_PRICE_FEATURE_COLUMNS]

    prediction = model.predict(input_df)[0]

    return round(float(prediction), 2)

def predict_price_from_model_file(
    model_path: str | Path,
    input_features: dict,) -> float:

    model = load_model(model_path)
    return predict_price(model, input_features)
