from pydantic import BaseModel
from typing import List
from datetime import date


class OrderRequest(BaseModel):
    create_day: date
    phonenumber: str
    andress: str
    total_price: float
    status: str
    description: str
    customer_id: int
    employee_id: int




class Order(BaseModel):
    id: int
    create_day: date
    phonenumber: str
    andress: str
    total_price: float
    status: str
    description: str
    customer_id: int
    employee_id: int

    class Config:
        orm_mode = True


class OrderResponse(BaseModel):
    data: List[Order]
    page: int
    size: int
    total_page: int
    total_record: int

    class Config:
        orm_mode = True