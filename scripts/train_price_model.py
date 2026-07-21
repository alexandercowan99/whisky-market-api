from pathlib import Path

import pandas as pd

from app.ml.training import train_and_save_price_model
from app.services.cleaning import add_cleaned_columns


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DEFAULT_INPUT_CSV_PATH = PROJECT_ROOT / "data" / "sample" / "sample_auction_lots.csv"
DEFAULT_MODEL_PATH = PROJECT_ROOT / "models" / "price_model.joblib"

def main() -> None:
    raw_df = pd.read_csv(DEFAULT_INPUT_CSV_PATH)

    cleaned_df = add_cleaned_columns(raw_df)

    metrics = train_and_save_price_model(
        cleaned_df=cleaned_df,
        model_path=DEFAULT_MODEL_PATH,
    )

    print("Model training complete")
    print(metrics)

if __name__ == "__main__":
    main()