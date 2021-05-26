from typing import Optional

from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from app.common.dependencies import get_db, validate_user
from app.repository import employee_repository
from app.schemas import employee_schemas

router = APIRouter(
    tags=['Employee'],
    prefix="/employee"
)


@router.post('/create_employee/')
def create_employee(request: employee_schemas.EmployeeRequest, token: Optional[str] = Header(None),
                    db: Session = Depends(get_db)):
    if token is None:
        return "Please login for this action"
    else:
        role: str = validate_user(token=token)
    if role is not None and role == "emp":
        employee_repository.create_employee(db=db, employee=request)
        return "Employee is added"
    elif role != "emp":
        return "You don't have permission"


@router.get('/get_all_employee/', response_model=employee_schemas.EmployeeResponse)
def get_all_employee(page: int, size: int, db: Session = Depends(get_db)):
    return employee_repository.get_all_employee(db=db, page=page, size=size)


@router.get('/get_employee_by_keyword/', response_model=employee_schemas.EmployeeResponse)
def get_employee_by_keyword(page: int, size: int, keyword: Optional[str] = None, db: Session = Depends(get_db)):
    return employee_repository.get_customer_by_keyword(db=db, page=page, size=size, keyword=keyword)


@router.put('/update_employee/')
def update_employee(request: employee_schemas.EmployeeRequest, id: int, token: Optional[str] = Header(None),
                    db: Session = Depends(get_db)):
    if token is None:
        return "Please login for this action"
    else:
        role: str = validate_user(token=token)
    if role is not None and role == "emp":
        employee_repository.update_employee(db=db, id=id, employee=request)
        return "Employee is updated"
    elif role != "emp":
        return "You don't have permission"


@router.delete('/delete_employee/')
def delete_employee(id: int, token: Optional[str] = Header(None), db: Session = Depends(get_db)):
    if token is None:
        return "Please login for this action"
    else:
        role: str = validate_user(token=token)
    if role is not None and role == "emp":
        employee_repository.delete_employee(db=db, id=id)
        return "Employee is deleted"
    elif role != "emp":
        return "You don't have permission"
