from typing import Optional

from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from app.common.dependencies import get_db, validate_user
from app.repository import customer_repository
from app.schemas import customer_schemas

router = APIRouter(
    tags=['Customer'],
    prefix="/customer"
)


@router.post('/create_customer/')
def create_customer(request: customer_schemas.CustomerRequest, token: Optional[str] = Header(None),
                    db: Session = Depends(get_db)):
    if token is None:
        return "Please login for this action"
    else:
        role: str = validate_user(token=token)
    if role is not None and role == "user":
        customer_repository.create_customer(db=db, customer=request)
        return "Customer is added"
    elif role != "user":
        return "You don't have permission"


@router.get('/get_all_customer/', response_model=customer_schemas.CustomerResponse)
def get_all_customer(page: int, size: int, db: Session = Depends(get_db)):
    return customer_repository.get_all_customer(db=db, page=page, size=size)


@router.get('/get_customer_by_keyword/', response_model=customer_schemas.CustomerResponse)
def get_customer_by_keyword(page: int, size: int, keyword: Optional[str] = None, db: Session = Depends(get_db)):
    return customer_repository.get_customer_by_keyword(db=db, page=page, size=size, keyword=keyword)


@router.put('/update_customer/')
def update_customer(request: customer_schemas.CustomerRequest, id: int, token: Optional[str] = Header(None),
                    db: Session = Depends(get_db)):
    if token is None:
        return "Please login for this action"
    else:
        role: str = validate_user(token=token)
    if role is not None and role == "user":
        customer_repository.update_customer(db=db, customer=request, id=id)
        return "Customer is updated"
    elif role != "user":
        return "You don't have permission"


@router.delete('/delete_customer/')
def delete_customer(id: int, token: Optional[str] = Header(None), db: Session = Depends(get_db)):
    if token is None:
        return "Please login for this action"
    else:
        role: str = validate_user(token=token)
    if role is not None and role == "user":
        customer_repository.delete_customer(db=db, id=id)
        return "Customer is deleted"
    elif role != "user":
        return "You don't have permission"
