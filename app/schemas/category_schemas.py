from pydantic import BaseModel
from typing import Optional, List


class CategoryRequest(BaseModel):
    name: str
    description: Optional[str] = None


class Category(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    class Config:
        orm_mode = True



class CategoryResponse(BaseModel):
    data: List[Category]
    page: int
    size: int
    total_page: int
    total_record: int

    class Config:
        orm_mode = True