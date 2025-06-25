from pydantic import BaseModel
from typing import List

class FeatureVector(BaseModel):
    vector: List[float]
