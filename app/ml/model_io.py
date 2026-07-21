from pathlib import Path
from typing import Any

import joblib

def save_model(model: Any, model_path: str | Path) -> None:

    model_path = Path(model_path)
    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, model_path)


def load_model(model_path: str | Path) -> Any:
    
    model_path = Path(model_path)
    return joblib.load(model_path)