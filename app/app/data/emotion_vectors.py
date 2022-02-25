from functools import lru_cache

import numpy as np

from core.config import settings
from data.base import BaseDataset


class EmotionVectorDataset(BaseDataset):
    name: str = settings.EMOTION_VECTOR_DATA
    path: str
    _dataset: np.ndarray

    def __init__(self):
        super().__init__()
        self._dataset = np.load(f"{self.path}.npy")

    @property
    def dataset(self) -> np.ndarray:
        return self._dataset


@lru_cache
def get_emotion_vector_dataset() -> EmotionVectorDataset:
    return EmotionVectorDataset()

