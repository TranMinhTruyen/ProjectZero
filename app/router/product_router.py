from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session


from app.common.dependencies import get_db
from app.repository import product_repository
from app.schemas import product_schemas
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(
    tags=['Product'],
    prefix="/product"
)


@router.post('/create_product', response_model=product_schemas.Product)
def create_product(request: product_schemas.ProductRequest, db: Session = Depends(get_db)):
    """
        Create an item with all the information:

        - **name**: each item must have a name
        - **price**: required
        - **category_id**: each item must have a category
        - **brand_id**: each item must have a brand
    """
    return product_repository.create_product(db=db, product=request)


@router.get('/get_all_product')
def get_all_product(page: int, size: int, db: Session = Depends(get_db)):
    return product_repository.get_all_product(db=db, page=page, size=size)


@router.get('/get_product_by_keyword')
def get_product_by_keyword(page: int, size: int, keyword: Optional[str] = None, db: Session = Depends(get_db)):
    return product_repository.get_product_by_keyword(db, page=page, size=size, keyword=keyword)


@router.put('/update_product')
def update_product(product: product_schemas.ProductRequest, id: int, db: Session = Depends(get_db)):
    return product_repository.update_product(db=db, product=product, id=id)


@router.delete('/delete_product')
def delete_product(id: int, db: Session = Depends(get_db)):
    return product_repository.delete_product(db=db, id=id)