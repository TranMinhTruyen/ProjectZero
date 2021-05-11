from pydantic import BaseModel
from typing import List
from datetime import date


class CustomerRequest(BaseModel):
    account: str
    password: str
    firstname: str
    lastname: str
    birthday: date
    phonenumber: str
    andress: str
    is_active: str




class Customer(BaseModel):
    id: int
    firstname: str
    lastname: str
    birthday: date
    phonenumber: str
    andress: str
    is_active: str

    class Config:
        orm_mode = True


class CustomerResponse(BaseModel):
    data: List[Customer]
    page: int
    size: int
    total_page: int
    total_record: int

    class Config:
        orm_mode = True