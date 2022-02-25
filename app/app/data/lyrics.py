from functools import lru_cache
from typing import Union

from core.config import settings
from data.base import BaseDataset
from datasets import Dataset, DatasetDict, load_from_disk


class LyricsDataset(BaseDataset):
    name: str = settings.LYRICS_DATA
    path: str
    _dataset: Union[Dataset, DatasetDict]

    def __init__(self):
        super().__init__()
        self._dataset = load_from_disk(self.path)

    @property
    def dataset(self) -> Union[Dataset, DatasetDict]:
        return self._dataset


@lru_cache
def get_lyrics_dataset() -> LyricsDataset:
    return LyricsDataset()
