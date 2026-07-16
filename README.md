## System Components

1. **Frontend** [Not Started] — user-facing web interface for uploading images and visualizing orientation estimation results.
2. **Backend for Frontend (BFF)** [Not Started] — API layer that mediates between the frontend and the underlying services (feature extraction, model inference, storage).
3. **Orientation Estimator** [Deployed] — SVM RBF model that estimates de 3D orientation of objects from classical computer vision features extracted from RGB images.
4. **Feature Database** [Not Started] — persistence layer storing extracted image features (Hu moments, HOG, geometric metrics) and associated metadata.
5. **Images and Masks Storage** [Not Started] — object storage for raw input images and segmentation masks used in the feature extraction pipeline.

---

# Visual Orientation Estimation System — Orientation Estimator Service

Inference service for estimating the 3D orientation of objects from classical computer vision features extracted from RGB images.

## What the service does

Given a feature vector extracted from an image (Hu moments, Histogram of Oriented Gradients — HOG, geometric metrics of the object's contour), the service returns the object's estimated 3D orientation, represented as a **canonicalized unit quaternion** (`qw ≥ 0`).

Based on the **Linemod/BOP** benchmark (`object_id=4`, a camera), part of a master's research project in signal processing and instrumentation (PPGEE/UFRGS).

## Access

| Item | Value |
|---|---|
| Hosted on | Google Cloud Run function |
| Endpoint | `https://visual-orientation-estimator-<hash>.southamerica-east1.run.app` |
| Method | `POST` |
| Authentication | Google identity token in the `Authorization: Bearer <ID_TOKEN>` header |

### Request format

```json
{
  "x": {
    "compactness_ext": "float",
    "dist_centroid": "float",
    "angle_centroid": "float",
    "sin_centroid": "float",
    "cos_centroid": "float",
    "aspect_ratio": "float",
    "eccentricity": "float",
    "sin_major": "float",
    "cos_major": "float",
    "hog_0_30": "float",
    "hog_30_60": "float",
    "hog_60_90": "float",
    "hog_90_120": "float",
    "hog_120_150": "float",
    "hog_150_180": "float",
    "hog_180_210": "float",
    "hog_210_240": "float",
    "hog_240_270": "float",
    "hog_270_300": "float",
    "hog_300_330": "float",
    "hog_330_360": "float",
    "hu_1": "float",
    "hu_2": "float",
    "hu_3": "float",
    "hu_4": "float",
    "hu_5": "float",
    "hu_6": "float",
    "hu_7": "float"
  },
  "y": {
    "qw": "float",
    "qx": "float",
    "qy": "float",
    "qz": "float"
  }
}
```

- **`x`** (required): the model's 28 input features.
- **`y`** (optional): ground-truth quaternion. If provided, the service also returns the geodesic error between the prediction and the true value.

### Response format

```json
{
  "qw": "float",
  "qx": "float",
  "qy": "float",
  "qz": "float",
  "geodesic_error": "float"
}
```

`geodesic_error` (in degrees) is only returned when `y` is included in the request.

## Machine Learning model

| Item | Detail |
|---|---|
| Algorithm | SVM (Support Vector Machine) with RBF kernel |
| Pipeline | Preprocessor (scaler) → Estimator (SVM) |
| Output representation | Canonicalized unit quaternion (`qw ≥ 0`) |
| Evaluation metric | Angular geodesic error, in degrees |
| Performance | ~5.3° mean geodesic error on the test set |
| Input features | Hu moments (7), HOG (12 angular bins), contour geometric metrics (9) |
| Serialization | `joblib` (`model.pkl` + `preprocessor.pkl`) |

## Tech stack

- **Function framework**: `functions-framework`
- **ML**: `scikit-learn`
- **Data validation**: `pydantic`
- **Data handling**: `pandas`, `numpy`
- **Build/Deploy**: Google Cloud Buildpacks

## Code structure

```
orientation_estimator/
├── main.py                          # HTTP entry point (estimate_orientation)
├── requirements.txt
├── models/
│   └── object_4/
│       └── svm_rbf/
│           ├── model.pkl
│           └── preprocessor.pkl
└── utils/
    ├── inference_utils.py           # Model loading (with caching) and quaternion utilities
    ├── evaluation_utils.py          # Geodesic error calculation
    └── interface_utils.py           # Pydantic schemas (PredictionRequest, ModelInputs, etc.)
```

## Testing locally

A test script is available at `tests/orientation_estimator_tests/`, which reads the service URL from a local `config.json` (not versioned), generates an identity token via `gcloud auth print-identity-token`, and sends requests to predict the dataset's test split.

Required configuration (`config.json`, at the project root — use `config.json.example` as a template):

```json
{
  "orientation_estimator_url": "https://visual-orientation-estimator-<hash>.southamerica-east1.run.app"
}
```