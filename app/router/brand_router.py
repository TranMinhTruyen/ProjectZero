from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.common.dependencies import get_db
from app.schemas import brand_schemas
from app.repository import brand_repository

router = APIRouter(
    tags=['Brand'],
    prefix="/brand"
)


@router.post('/create_brand')
def create_brand(request: brand_schemas.BrandRequest, db: Session = Depends(get_db)):
    return brand_repository.create_brand(db=db, brand=request)


@router.get('/get_all_brand')
def get_all_brand(page: int, size: int, db: Session = Depends(get_db)):
    return brand_repository.get_all_brand(db=db, page=page, size=size)


@router.get('/get_brand_by_keyword')
def get_brand_by_keyword(page: int, size: int, keyword: Optional[str] = None, db: Session = Depends(get_db)):
    return brand_repository.get_brand_by_key_word(db, page=page, size=size, keyword=keyword)


@router.put('/update_brand')
def update_brand(request: brand_schemas.BrandRequest, id: int, db: Session = Depends(get_db)):
    return brand_repository.update_brand(db=db, brand=request, id=id)


@router.delete('/delete_brand')
def delete_brand(id: int, db: Session = Depends(get_db)):
    return brand_repository.delete_brand(db=db, id=id)