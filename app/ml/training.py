import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score


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