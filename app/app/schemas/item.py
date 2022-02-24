from typing import Optional

from pydantic import BaseModel


class ItemBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


class Item(ItemBase):
    pass
