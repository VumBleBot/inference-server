from api.v1.endpoints import inference
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(inference.router, tags=["inference"])
