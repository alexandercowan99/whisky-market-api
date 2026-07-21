import pandas as pd

NUMERIC_PRICE_FEATURE_COLUMNS = [
    "estimate_low",
    "estimate_high",
    "size_ml",
    "quantity",
]
TARGET_COLUMN = "result_price"

def build_price_training_dataset(cleaned_df: pd.DataFrame,) -> tuple[pd.DataFrame, pd.Series]:

    required_columns = NUMERIC_PRICE_FEATURE_COLUMNS + [TARGET_COLUMN]

    missing_columns = [
        column for column in required_columns
        if column not in cleaned_df.columns
    ]

    if len(missing_columns) > 0:
        raise ValueError(f"Missing required columns for ML training: {missing_columns}")
    
    model_df = cleaned_df[required_columns].dropna().copy()
    
    X = model_df[NUMERIC_PRICE_FEATURE_COLUMNS]
    y = model_df[TARGET_COLUMN]

    return X, y