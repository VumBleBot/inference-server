import os
from functools import lru_cache
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

    PROJECT_NAME: str

    class Config:
        case_sensitive = True
        env_file = str(os.path.join(Path(__file__).parent, f'env/{os.getenv("ENV_STATE", "dev")}.env'))
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()
