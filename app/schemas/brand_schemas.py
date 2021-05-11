from pydantic import BaseModel
from typing import Optional, List


class BrandRequest(BaseModel):
    name: str
    image: Optional[str] = None
    description: Optional[str] = None


class Brand(BaseModel):
    id: int
    name: str
    image: Optional[str] = None
    description: Optional[str] = None

    class Config:
        orm_mode = True


class BrandResponse(BaseModel):
    data: List[Brand]
    page: int
    size: int
    total_page: int
    total_record: int

    class Config:
        orm_mode = True