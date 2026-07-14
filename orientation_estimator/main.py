import functions_framework
from pydantic import ValidationError
from utils.evaluation_utils import geodesic_error
from utils.inference_utils import load_model, normalize_quarternion
from utils.interface_utils import PredictionRequest, PredictionResponse
import numpy as np
import pandas as pd

X_cols = [
    'compactness_ext',
    'dist_centroid',
    'angle_centroid',
    'sin_centroid',
    'cos_centroid',
    'aspect_ratio',
    'eccentricity',
    'sin_major',
    'cos_major',
    'hog_0_30',
    'hog_30_60',
    'hog_60_90',
    'hog_90_120',
    'hog_120_150',
    'hog_150_180',
    'hog_180_210',
    'hog_210_240',
    'hog_240_270',
    'hog_270_300',
    'hog_300_330',
    'hog_330_360',
    'hu_1',
    'hu_2',
    'hu_3',
    'hu_4',
    'hu_5',
    'hu_6',
    'hu_7',
]


@functions_framework.http
def estimate_orientation(request):
    if request.method != "POST":
        return {"error": "Method not allowed. Use POST."}, 405, {"Allow": "POST"}

    body = request.get_json(silent=True)
    if body is None:
        return {"error": "Request body must be valid JSON."}, 400

    try:
        payload = PredictionRequest(**body)
    except ValidationError as e:
        return {"error": e.errors()}, 400

    X = pd.DataFrame([payload.model_dump()])[X_cols]
    print(X.head(1))
    y_true = payload.to_output_vector()

    model = load_model()
    y_pred = normalize_quarternion(model.predict(X)[0])
    print(f"Geodesic error: {y_true, y_pred, geodesic_error(y_true, y_pred)}")
    
    y_cols = ['qw', 'qx', 'qy', 'qz']
    response_payload = {}
    for i, y_col in enumerate(y_cols):
        response_payload[y_col] = y_pred[i]
    #response = PredictionResponse(**response_payload)

    return response_payload