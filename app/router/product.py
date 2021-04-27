from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.common.dependencies import get_db
from app.repository import product_repository
from app.schemas import product_schemas

router = APIRouter(
    tags=['Product'],
    prefix="/product"
)


@router.get('/get_all_product', response_model=List[product_schemas.ShowProduct])
def get_all_product(db: Session = Depends(get_db)):
    return product_repository.get_all(db)
