from api.v1.api import api_router
from core.config import get_settings
from fastapi import FastAPI

settings = get_settings()

app = FastAPI(title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json")

app.include_router(api_router, prefix=settings.API_V1_STR)
