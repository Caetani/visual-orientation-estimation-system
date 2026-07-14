from pathlib import Path
import joblib
from sklearn.base import BaseEstimator
from sklearn.pipeline import Pipeline
import numpy as np

BASE_DIR = Path(__file__).resolve().parent.parent
_model_cache: dict[str, BaseEstimator] = {}

def load_model(
    model_name: str = "svm_rbf",
    object_id: int = 4,
) -> BaseEstimator:
    cache_key = f"{object_id}_{model_name}"

    if cache_key not in _model_cache:
        model_file = BASE_DIR / "models" / f"object_{object_id}" / model_name / "model.pkl"
        preprocessor_file = BASE_DIR / "models" / f"object_{object_id}" / model_name / "preprocessor.pkl"

        if not model_file.exists():
            raise FileNotFoundError(f"Model file not found: {model_file}")

        model = joblib.load(model_file)

        if preprocessor_file.exists():
            preprocessor = joblib.load(preprocessor_file)
            model = Pipeline(steps=[
                ('preprocessor', preprocessor),
                ('estimator', model)
            ])

        _model_cache[cache_key] = model

    return _model_cache[cache_key]



def normalize_quarternion(q):
    return q / np.linalg.norm(q)