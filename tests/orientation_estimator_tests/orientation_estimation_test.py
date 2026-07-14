import sys
from pathlib import Path

SERVICE_ROOT = Path(__file__).resolve().parents[2] / "orientation_estimator"
sys.path.insert(0, str(SERVICE_ROOT))

import numpy as np
import pandas as pd
import requests

from utils.evaluation_utils import geodesic_error
from utils.interface_utils import PredictionRequest

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

y_cols = ['qw', 'qx', 'qy', 'qz']

URL = "http://localhost:8080"


if __name__ == '__main__':
    DATA_DIR = SERVICE_ROOT / '..' / 'data' / 'splitted_train_70_30.xlsx'

    df = pd.read_excel(DATA_DIR)
    df_test = df[(df['set'] == 'test') & (df['object_id'] == 4)]

    #print(df_test)
    #exit()

    X_test, y_test = df_test[X_cols], df_test[y_cols]

    errors = []
    failed = []

    counter = 1
    for idx, row in df_test.iterrows():
        print(counter)
        counter += 1
        # Validate locally first, so a malformed row fails fast with a clear
        # Pydantic error instead of a confusing HTTP 400 from the server.
        payload = PredictionRequest(**row[X_cols + y_cols].to_dict())

        response = requests.post(URL, json=payload.model_dump())

        if response.status_code != 200:
            print(f"[{idx}] request failed: {response.status_code} {response.text}")
            failed.append(idx)
            continue

        result = response.json()
        q_pred = np.array(
            [result["qw"], result["qx"], result["qy"], result["qz"]],
            dtype=np.float64,
        )
        q_true = y_test.loc[idx, y_cols].to_numpy(dtype=np.float64)

        error_deg = geodesic_error(q_true, q_pred)
        errors.append(error_deg)

    errors = np.array(errors)

    print(f"Test set size: {len(X_test)}")
    print(f"Successful requests: {len(errors)}")
    print(f"Failed requests: {len(failed)}")
    print(f"Mean geodesic error:   {errors.mean():.3f} deg")
    print(f"Std geodesic error:    {errors.std():.3f} deg")
    print(f"Median geodesic error: {np.median(errors):.3f} deg")
    print(f"Max geodesic error:    {errors.max():.3f} deg")