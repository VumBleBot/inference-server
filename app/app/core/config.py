import os
from pathlib import Path

from pydantic import AnyHttpUrl, BaseSettings


class Settings(BaseSettings):
    ROOT_DIR: str = str(os.path.join(Path(__file__).parent.parent.parent, "app"))
    PROJECT_DIR: str = os.path.join(ROOT_DIR, "app")

    APP_ENV: str = "dev"
    API_V1_STR: str = "/api/v1"
    SERVER_NAME: str
    SERVER_HOST: AnyHttpUrl
    SERVER_PORT: int
    USE_ES: bool = False
    ES_HOST: str = ""
    ES_PORT: int = 9200

    PROJECT_NAME: str

    TOPK: int = 30
    LYRICS_DATA: str
    EMOTION_VECTOR_DATA: str

    class Config:
        case_sensitive = True
        env_file = str(os.path.join(Path(__file__).parent, f'env/{os.getenv("ENV_STATE", "dev")}.env'))
        env_file_encoding = "utf-8"


settings = Settings()
