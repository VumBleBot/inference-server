from typing import Optional

import numpy.typing
from pydantic import BaseModel

class EmotionVector(BaseModel):
    label: str
    vector: numpy.typing.NDArray
