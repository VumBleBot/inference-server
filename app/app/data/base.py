import os
from abc import ABCMeta, abstractmethod
from pathlib import Path


class BaseDataset(metaclass=ABCMeta):
    name: str
    path: str

    @abstractmethod
    def __init__(self):
        current_dir = Path(__file__).parent
        asset_dir = os.path.join(current_dir, "assets")
        self.path = os.path.join(asset_dir, self.name)
