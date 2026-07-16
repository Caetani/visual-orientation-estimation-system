from pydantic import BaseModel

class ModelInputs(BaseModel):
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

    def to_vector(self) -> list:
        return [getattr(self, name) for name in type(self).model_fields]


class ModelOutputs(BaseModel):
    qw: float
    qx: float
    qy: float
    qz: float

    def to_vector(self) -> list:
        return [getattr(self, name) for name in type(self).model_fields]


class PredictionRequest(BaseModel):
    x: ModelInputs
    y: ModelOutputs

    def to_feature_vector(self) -> list:
        return self.x.to_vector()

    def to_output_vector(self) -> list:
        return self.y.to_vector()
    

class PredictionResponse(BaseModel):
    qw: float
    qx: float
    qy: float
    qz: float
    geodesic_error: float

