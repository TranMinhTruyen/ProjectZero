from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.common.dependencies import get_db
from app.schemas import category_schemas
from app.repository import category_repository

router = APIRouter(
    tags=['Category'],
    prefix="/category"
)


@router.post('/create_category')
def create_category(request: category_schemas.CategoryRequest, db: Session = Depends(get_db)):
    return category_repository.create_category(db=db, category=request)


@router.get('/get_all_category')
def get_all_category(page: int, size: int, db: Session = Depends(get_db)):
    return category_repository.get_all_category(db=db, page=page, size=size)


@router.get('/get_category_by_keyword')
def get_category_by_keyword(page: int, size: int, keyword: Optional[str] = None, db: Session = Depends(get_db)):
    return category_repository.get_category_by_key_word(db, page=page, size=size, keyword=keyword)


@router.put('/update_category')
def update_category(request: category_schemas.CategoryRequest, id: int, db: Session = Depends(get_db)):
    return category_repository.update_category(db=db, category=request, id=id)


@router.delete('/delete_category')
def delete_category(id: int, db: Session = Depends(get_db)):
    return category_repository.delete_category(db=db, id=id)
