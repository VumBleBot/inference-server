from typing import Any, List

import schemas
from fastapi import APIRouter

router = APIRouter()

# sample endpoints


@router.get("/", response_model=List[schemas.Item])
def sample_endpoint() -> Any:
    """
    sample endpoint
    :return:
    """
    item = schemas.Item(title="sample item", description="sample_description")
    return [item]
