from pathlib import Path

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

from app.ml.features import build_price_training_dataset
from app.ml.model_io import save_model

def train_baseline_price_model(X: pd.DataFrame,y: pd.Series,) -> tuple[LinearRegression, dict]:

    model = LinearRegression()

    model.fit(X, y)

    predictions = model.predict(X)

    mae = mean_absolute_error(y, predictions)

    r2 = r2_score(y, predictions)

    return model, {
    "training_rows": len(X),
    "mae": round(float(mae), 2),
    "r2": round(float(r2), 4),
    }

def train_evaluate_baseline_price_model(X: pd.DataFrame,y: pd.Series,test_size: float = 0.25,random_state: int = 42,) -> tuple[LinearRegression, dict]:
    
    X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=test_size,
    random_state=random_state,
    )

    model = LinearRegression()
    model.fit(X_train, y_train)

    train_predictions = model.predict(X_train)
    test_predictions = model.predict(X_test)

    train_mae = mean_absolute_error(y_train, train_predictions)
    test_mae = mean_absolute_error(y_test, test_predictions)
    test_r2 = r2_score(y_test, test_predictions)

    return model, {
        "training_rows": len(X_train),
        "test_rows": len(X_test),
        "train_mae": round(float(train_mae), 2),
        "test_mae": round(float(test_mae), 2),
        "test_r2": round(float(test_r2), 4),
    }

def train_and_save_price_model(
    cleaned_df: pd.DataFrame,
    model_path: str | Path,
    test_size: float = 0.25,
    random_state: int = 42,) -> dict:
    
    X, y = build_price_training_dataset(cleaned_df)

    X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=test_size,
    random_state=random_state,
    )

    model, metrics = train_evaluate_baseline_price_model(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
    )

    save_model(model, model_path)
    metrics["model_path"] = str(model_path)

    return metrics


