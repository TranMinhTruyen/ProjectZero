from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.common.dependencies import get_db, validate_user
from app.schemas import category_schemas
from app.repository import category_repository

router = APIRouter(
    tags=['Category'],
    prefix="/category"
)


@router.post('/create_category/{token}', response_model=category_schemas.Category)
def create_category(request: category_schemas.CategoryRequest, token: str, db: Session = Depends(get_db)):
    role: str = validate_user(token=token)
    if role is not None and role == "emp":
        return category_repository.create_category(db=db, category=request)
    else:
        return None


@router.get('/get_all_category/', response_model=category_schemas.CategoryResponse)
def get_all_category(page: int, size: int, db: Session = Depends(get_db)):
    return category_repository.get_all_category(db=db, page=page, size=size)


@router.get('/get_category_by_keyword/', response_model=category_schemas.CategoryResponse)
def get_category_by_keyword(page: int, size: int, keyword: Optional[str] = None, db: Session = Depends(get_db)):
    return category_repository.get_category_by_key_word(db, page=page, size=size, keyword=keyword)


@router.put('/update_category/{token}', response_model=category_schemas.Category)
def update_category(request: category_schemas.CategoryRequest, id: int, token: str, db: Session = Depends(get_db)):
    role: str = validate_user(token=token)
    if role is not None and role == "emp":
        return category_repository.update_category(db=db, category=request, id=id)
    else:
        return None


@router.delete('/delete_category/{token}')
def delete_category(id: int, token: str, db: Session = Depends(get_db)):
    role: str = validate_user(token=token)
    if role is not None and role == "emp":
        return category_repository.delete_category(db=db, id=id)
    else:
        return None
