from typing import List

from pydantic import BaseConfig, BaseModel, Field
from schemas.song import Song


class SongRecommendation(Song):
    ranking: int
    score: float


class RecommendationResponse(BaseModel):
    topk: int
    emotion_label: str
    emotion_score: float
    contents: List[SongRecommendation] = Field(default_factory=list)

    class Config:
        BaseConfig.arbitrary_types_allowed = True
        allow_population_by_field_name = True
