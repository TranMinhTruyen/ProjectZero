from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.common.dependencies import get_db, decode_access_token, get_password_hash
from app.repository import customer_repository
from app.schemas import customer_schemas, login_schemas

router = APIRouter(
    tags=['Customer'],
    prefix="/customer"
)


@router.post('/create_customer', response_model=customer_schemas.Customer)
def create_customer(request: customer_schemas.CustomerRequest, db: Session = Depends(get_db)):
    return customer_repository.create_customer(db=db, customer=request)


@router.post('/get_customer_info', response_model=customer_schemas.Customer)
def get_customer_info(token: login_schemas.Token, db=Depends(get_db)):
    payload: dict = decode_access_token(token=token.token)
    account: str = payload.get("account")
    password: str = payload.get("password")
    return customer_repository.get_customer_by_account_password(db=db,
                                                                account=account,
                                                                password=get_password_hash(password))


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
