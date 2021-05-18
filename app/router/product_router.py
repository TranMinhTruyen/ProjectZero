from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.common.dependencies import get_db, validate_user
from app.repository import product_repository
from app.schemas import product_schemas


router = APIRouter(
    tags=['Product'],
    prefix="/product"
)


@router.post('/create_product/{token}', response_model=product_schemas.Product)
def create_product(request: product_schemas.ProductRequest, token: str, db: Session = Depends(get_db)):
    role: str = validate_user(token=token)
    if role is not None and role == "emp":
        return product_repository.create_product(db=db, product=request)
    else:
        return None


@router.get('/get_all_product/', response_model=product_schemas.ProductResponse)
def get_all_product(page: int, size: int, db: Session = Depends(get_db)):
    return product_repository.get_all_product(db=db, page=page, size=size)


@router.get('/get_product_by_keyword/', response_model=product_schemas.ProductResponse)
def get_product_by_keyword(page: int, size: int, keyword: Optional[str] = None, db: Session = Depends(get_db)):
    return product_repository.get_product_by_keyword(db, page=page, size=size, keyword=keyword)


@router.put('/update_product/{token}', response_model=product_schemas.Product)
def update_product(product: product_schemas.ProductRequest, token: str, id: int, db: Session = Depends(get_db)):
    role: str = validate_user(token=token)
    if role is not None and role == "emp":
        return product_repository.update_product(db=db, product=product, id=id)
    else:
        return None


@router.delete('/delete_product/{token}')
def delete_product(id: int, token: str, db: Session = Depends(get_db)):
    role: str = validate_user(token=token)
    if role is not None and role == "emp":
        return product_repository.delete_product(db=db, id=id)
    else:
        return None
