from typing import Optional

from pydantic import BaseModel


class UserRequest(BaseModel):
    user_id: Optional[str]
    user_input: str
