import numpy as np
from pydantic import BaseModel


class Emotion(BaseModel):
    label: str
    score: float
    vector: np.ndarray

    class Config:
        arbitrary_types_allowed = True
