import numpy as np

def geodesic_error(q_true: np.ndarray, q_pred: np.ndarray) -> float:
    dot = np.dot(q_true, q_pred)
    dot = np.clip(np.abs(dot), 0.0, 1.0)
    return np.rad2deg(2 * np.arccos(dot))