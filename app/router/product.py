from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.common.dependencies import get_db
from app.services import product_services
from app.schemas import product_schemas

router = APIRouter(
    tags=['Product'],
    prefix="/product"
)


# @router.get('/get_all_product', response_model=List[product_schemas.ShowProduct])
# def get_all_product(db: Session = Depends(get_db)):
#     return product_repository.get_all(db)


@router.get('/get_product_by_keyword')
def get_product_by_keyword(page: int, size: int, keyword: Optional[str] = None, db: Session = Depends(get_db)):
    return product_services.get_product_by_keyword(db, page=page, size=size, keyword=keyword)
