from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.common.dependencies import get_db
from app.repository import employee_repository
from app.schemas import employee_schemas

router = APIRouter(
    tags=['Employee'],
    prefix="/employee"
)


@router.post('/create_employee', response_model=employee_schemas.Employee)
def create_employee(request: employee_schemas.EmployeeRequest, db: Session = Depends(get_db)):
    return employee_repository.create_employee(db=db, employee=request)




@router.get('/get_all_employee')
def get_all_employee(page: int, size: int, db: Session = Depends(get_db)):
    return employee_repository.get_all_employee(db=db, page=page, size=size)




@router.get('/get_employee_by_keyword')
def get_employee_by_keyword(page: int, size: int, keyword: Optional[str] = None, db: Session = Depends(get_db)):
    return employee_repository.get_customer_by_keyword(db=db, page=page, size=size, keyword=keyword)




@router.put('/update_employee')
def update_employee(request: employee_schemas.EmployeeRequest, id: int, db: Session = Depends(get_db)):
    return employee_repository.update_employee(db=db, id=id, employee=request)




@router.delete('/delete_employee')
def delete_employee(id: int, db: Session = Depends(get_db)):
    return employee_repository.delete_employee(db=db, id=id)