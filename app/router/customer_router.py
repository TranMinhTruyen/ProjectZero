from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.common.dependencies import get_db
from app.repository import customer_repository
from app.schemas import customer_schemas


router = APIRouter(
    tags=['Customer'],
    prefix="/customer"
)




@router.post('/create_customer', response_model=customer_schemas.Customer)
def create_customer(request: customer_schemas.CustomerRequest, db: Session = Depends(get_db)):
    return customer_repository.create_customer(db=db, customer=request)




@router.get('/get_all_customer')
def get_all_customer(page: int, size: int, db: Session = Depends(get_db)):
    return customer_repository.get_all_customer(db=db, page=page, size=size)




@router.get('/get_customer_by_keyword')
def get_customer_by_keyword(page: int, size: int, keyword: Optional[str] = None, db: Session = Depends(get_db)):
    return customer_repository.get_customer_by_keyword(db=db, page=page, size=size, keyword=keyword)




@router.put('/update_customer')
def update_customer(request: customer_schemas.CustomerRequest, id: int, db: Session = Depends(get_db)):
    return customer_repository.update_customer(db=db, customer=request, id=id)




@router.delete('/delete_customer')
def delete_customer(id: int, db: Session = Depends(get_db)):
    return customer_repository.delete_customer(db=db, id=id)