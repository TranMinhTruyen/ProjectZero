from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.common.dependencies import get_db, validate_user
from app.repository import order_repository
from app.schemas import order_schemas

router = APIRouter(
    tags=['Order'],
    prefix="/order"
)


@router.get('/get_order_by_keyword/', response_model=order_schemas.OrderResponse)
def get_order_by_keyword(page: int, size: int, keyword: Optional[str] = None, db: Session = Depends(get_db)):
    return order_repository.get_order_by_keyword(db, page=page, size=size, keyword=keyword)


@router.get('/get_all_order/', response_model=order_schemas.OrderResponse)
def get_all_order(page: int, size: int, db: Session = Depends(get_db)):
    return order_repository.get_all_order(db=db, page=page, size=size)
