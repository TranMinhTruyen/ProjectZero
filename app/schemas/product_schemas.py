from pydantic import BaseModel
from typing import Optional, List


class ProductRequest(BaseModel):
    name: str
    price: float
    unit: str
    in_stock: int
    discount: Optional[int] = None
    image: Optional[str] = None
    description: Optional[str] = None
    brand_id: Optional[int] = None
    category_id: Optional[int] = None


class Product(BaseModel):
    id: int
    name: str
    price: float
    unit: str
    in_stock: int
    discount: Optional[int] = None
    image: Optional[str] = None
    description: Optional[str] = None
    brand_id: Optional[int] = None
    category_id: Optional[int] = None

    class Config:
        orm_mode = True


class ProductResponse(BaseModel):
    data: List[Product]
    page: int
    size: int
    total_page: int
    total_record: int

    class Config:
        orm_mode = True