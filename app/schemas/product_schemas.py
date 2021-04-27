from pydantic import BaseModel
from typing import Optional, List


class Product(BaseModel):
    id: int
    name: str
    price: float
    brand_id: Optional[int] = None
    category_id: Optional[int] = None

    class Config:
        orm_mode = True