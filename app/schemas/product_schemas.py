from pydantic import BaseModel


class Product(BaseModel):
    name: str
    price: float


class ShowProduct(Product):
    class Config:
        orm_mode = True
