import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_FILE = PROJECT_ROOT / "config.json"
SERVICE_ROOT = PROJECT_ROOT / "orientation_estimator"
sys.path.insert(0, str(SERVICE_ROOT))

import json
import numpy as np
import pandas as pd
import requests
import subprocess

with open(CONFIG_FILE) as f:
    config = json.load(f)

URL = config["orientation_estimator_url"]

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

def get_id_token() -> str:
    result = subprocess.run(
        ["gcloud", "auth", "print-identity-token"],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


if __name__ == '__main__':
    FRAME_ID = 502 # Between 0 and 1312
    OBJECT_ID = 4
    DATA_DIR = SERVICE_ROOT / '..' / 'data' / 'splitted_train_70_30.xlsx'

    df = pd.read_excel(DATA_DIR)
    df = df[df['object_id'] == OBJECT_ID]
    df_test = df[df['set'] == 'test']

    X_test, y_test = df_test[X_cols], df_test[y_cols]

    token = get_id_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    row = df[df['frame_id'] == FRAME_ID].iloc[0]

    input_features = {col: row[col] for col in X_cols}
    outputs = {col: row[col] for col in y_cols}

    payload = {
        'x': input_features,
        'y': outputs
    }

    response = requests.post(url=URL, json=payload, headers=headers, timeout=30)

    if response.status_code != 200:
        print(f"[Request failed: {response.status_code} {response.text}")

    result = response.json()

    q_pred = np.array(
        [result["qw"], result["qx"], result["qy"], result["qz"]],
        dtype=np.float64,
    )

    print(f"\nFrame: {FRAME_ID}\n\tPredicted quarternion: {q_pred}\n\tGeodesic error = {result['geodesic_error']} degrees.\n")