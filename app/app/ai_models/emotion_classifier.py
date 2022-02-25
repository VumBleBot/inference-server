import json
import os
from functools import lru_cache
from pathlib import Path

import torch
import torch.nn as nn
from schemas.emotion import Emotion
from transformers import AutoModel, BertTokenizerFast


class EmotionClassifier(nn.Module):
    task_name = "emotion_analysis"

    def __init__(self):
        super().__init__()
        current_dir = Path(__file__).parent
        asset_dir = os.path.join(current_dir, self.task_name)

        model_path = os.path.join(asset_dir, "model.pth")
        label_path = os.path.join(asset_dir, "label.json")

        model_path_or_name = "kykim/albert-kor-base"

        self.albert = AutoModel.from_pretrained(model_path_or_name)
        self.tokenizer = BertTokenizerFast.from_pretrained(model_path_or_name)
        self.classifier = nn.Linear(self.albert.config.hidden_size, 60)

        self._load_model(model_path)
        self._load_label(label_path)

    def _load_model(self, model_path: str) -> None:
        assert os.path.exists(model_path), f"{model_path}가 존재하지 않습니다"
        self.load_state_dict(torch.load(model_path, map_location=torch.device("cpu")))

    def _load_label(self, label_path: str) -> None:
        assert os.path.exists(label_path), f"{label_path}가 존재하지 않습니다"
        self.idx2label = json.load(open(label_path, "r"))

    def vector_to_label(self, emotion_vector: torch.Tensor) -> str:
        """emotion_vector의 label을 출력합니다"""
        idx = self.classifier(emotion_vector).detach().argmax(-1).cpu().item()
        return self.idx2label[str(idx)]

    def forward(self, inputs: str) -> torch.Tensor:
        """emotion vector를 return합니다"""
        inputs = self.tokenizer(
            [inputs], truncation=True, max_length=256, return_tensors="pt"
        )  # inputs: batch that length is one
        emotion_vector = self.albert(**inputs)[0][:, 0]  # cls token
        return emotion_vector

    async def predict(self, input: str) -> Emotion:
        with torch.no_grad():
            input_vector = self.forward(input)
            label = self.vector_to_label(input_vector)
            input_vector = input_vector.detach().numpy()
        return Emotion(label=label, vector=input_vector)


@lru_cache
def get_emotion_classifier() -> EmotionClassifier:
    return EmotionClassifier()
