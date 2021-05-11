from pydantic import BaseModel
from typing import List
from datetime import date



class EmployeeRequest(BaseModel):
    account: str
    password: str
    firstname: str
    lastname: str
    birthday: date
    citizen_id: str
    phonenumber: str
    andress: str
    is_active: str




class Employee(BaseModel):
    id: int
    account: str
    password: str
    firstname: str
    lastname: str
    birthday: date
    citizen_id: str
    phonenumber: str
    andress: str
    is_active: str

    class Config:
        orm_mode = True


class EmployeeResponse(BaseModel):
    data: List[Employee]
    page: int
    size: int
    total_page: int
    total_record: int

    class Config:
        orm_mode = True