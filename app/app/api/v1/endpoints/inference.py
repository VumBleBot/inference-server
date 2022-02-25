from typing import Any

import numpy as np
from ai_models.emotion_classifier import get_emotion_classifier
from ai_models.retriever import RetrieverType, get_retriever
from core.config import settings
from data.emotion_vectors import get_emotion_vector_dataset
from data.lyrics import get_lyrics_dataset
from fastapi import APIRouter
from schemas.recommendation import RecommendationResponse, SongRecommendation
from schemas.user_request import UserRequest

router = APIRouter()

emotion_classifier = get_emotion_classifier()
retriever = get_retriever(type=RetrieverType.CUSTOM)


@router.post("/inference", response_model=RecommendationResponse)
async def inference(request: UserRequest) -> Any:
    """
    발화 문장을 통하여 사용자의 감정을 분류하고,
    감정 벡터공간과 가사 데이터베이스를 이용하여 사용자의 감정과 연관있는 노래 리스트를 추천한다.
    :param:
    UserRequest
    - user_id: str, 비식별처리된 uuid
      user_input: str, 사용자가 입력한 발화문장
    :return:
    RecommendationResponse
    - topk: 후보 갯수
      emotion_label: 감정 레이블
      List[SongRecommendation]
        - ranking: 후보군 중 순위
          score: 추천 스코어
          artist: 노래 가수
          song_name : 노래 제목
    """
    print(request.user_input)
    user_input = request.user_input

    # Emotion Analysis
    # emotion_classifier = get_emotion_classifier()
    emotion_classifier.eval()
    user_emotion = await emotion_classifier.predict(user_input)

    # Retrieval
    # TODO Add Retriever type change by env
    # retriever = get_retriever(type=RetrieverType.CUSTOM)
    # TODO exception handling for retrieval fail
    indices = await retriever.get_relevant_doc_bulk(query=user_input, topk=settings.TOPK)

    # Dataset
    lyrics_dataset = get_lyrics_dataset()
    print(f"LOAD LYRICS DATA : [{lyrics_dataset.name}]")
    candidate_lyrics = lyrics_dataset.dataset[indices]

    emotion_vector_dataset = get_emotion_vector_dataset()
    print(f"LOAD EMOTION VECTOR DATA : [{emotion_vector_dataset.name}]")
    candidate_vectors = emotion_vector_dataset.dataset[indices]

    # sort candidates
    # TODO change cosine similarity by env
    emotion_inner_product = map(lambda x: np.dot(user_emotion.vector, x), candidate_vectors)
    score_indices, sorted_scores = zip(*sorted(enumerate(emotion_inner_product), key=lambda x: x[1], reverse=True))

    print(f"User Input : {user_input}")
    print(f"Emotion Label of User : {user_emotion.label}")

    response = RecommendationResponse(topk=settings.TOPK, emotion_label=user_emotion.label, contents=[])

    for index, score in zip(score_indices, sorted_scores):
        artist = candidate_lyrics["artists"][index]
        song_name = candidate_lyrics["song_name"][index]

        response.contents.append(SongRecommendation(ranking=index, score=score, artist=artist, song_name=song_name))

    print("Recommendation Complete.")
    print(f"Best Recommendation : {response.contents[0].artist} - {response.contents[0].song_name}")
    print(f"Recommendation Score : {response.contents[0].score}")

    return response


# TODO
# Health check api after model loading
