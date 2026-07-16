import functions_framework
from pydantic import ValidationError
from utils.evaluation_utils import geodesic_error
from utils.inference_utils import load_model, normalize_quarternion
from utils.interface_utils import PredictionRequest, PredictionResponse, ModelInputs, ModelOutputs
import numpy as np
import pandas as pd

x_cols = ModelInputs.model_fields.keys()
y_cols = ModelOutputs.model_fields.keys()

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

    x = pd.DataFrame([payload.x.model_dump()])[x_cols]
    y_true = payload.to_output_vector()

    model = load_model()
    y_pred = normalize_quarternion(model.predict(x)[0])
    
    response_payload = {}
    for i, y_col in enumerate(y_cols):
        response_payload[y_col] = y_pred[i]

    response_payload['geodesic_error'] = geodesic_error(y_true, y_pred)

    response = PredictionResponse(**response_payload)

    return response.model_dump_json(), 200