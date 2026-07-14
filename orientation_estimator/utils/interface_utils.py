from pydantic import BaseModel
import numpy as np

class PredictionRequest(BaseModel):
    compactness_ext: float
    dist_centroid: float
    angle_centroid: float
    sin_centroid: float
    cos_centroid: float
    aspect_ratio: float
    eccentricity: float
    sin_major: float
    cos_major: float
    hog_0_30: float
    hog_30_60: float
    hog_60_90: float
    hog_90_120: float
    hog_120_150: float
    hog_150_180: float
    hog_180_210: float
    hog_210_240: float
    hog_240_270: float
    hog_270_300: float
    hog_300_330: float
    hog_330_360: float
    hu_1: float
    hu_2: float
    hu_3: float
    hu_4: float
    hu_5: float
    hu_6: float
    hu_7: float
    qw: float
    qx: float
    qy: float
    qz: float

    def to_feature_vector(self) -> list:
        return [
            self.compactness_ext,
            self.dist_centroid,
            self.angle_centroid,
            self.sin_centroid,
            self.cos_centroid,
            self.aspect_ratio,
            self.eccentricity,
            self.sin_major,
            self.cos_major,
            self.hog_0_30,
            self.hog_30_60,
            self.hog_60_90,
            self.hog_90_120,
            self.hog_120_150,
            self.hog_150_180,
            self.hog_180_210,
            self.hog_210_240,
            self.hog_240_270,
            self.hog_270_300,
            self.hog_300_330,
            self.hog_330_360,
            self.hu_1,
            self.hu_2,
            self.hu_3,
            self.hu_4,
            self.hu_5,
            self.hu_6,
            self.hu_7,
        ]
    

    def to_output_vector(self) -> list:
        return np.array([
            self.qw,
            self.qx,
            self.qy,
            self.qz
        ])

class PredictionResponse(BaseModel):
    qw: float
    qx: float
    qy: float
    qz: float
    #yaw_deg: float
    #pitch_deg: float
    #roll_deg: float
    #geodesic_error_deg: float