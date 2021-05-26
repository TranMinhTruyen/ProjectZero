from typing import Optional

from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from app.common.dependencies import get_db, validate_user
from app.schemas import category_schemas
from app.repository import category_repository

router = APIRouter(
    tags=['Category'],
    prefix="/category"
)


@router.post('/create_category/')
def create_category(request: category_schemas.CategoryRequest, token: Optional[str] = Header(None),
                    db: Session = Depends(get_db)):
    if token is None:
        return "Please login for this action"
    else:
        role: str = validate_user(token=token)
    if role is not None and role == "emp":
        category_repository.create_category(db=db, category=request)
        return "Category is added"
    elif role != "emp":
        return "You don't have permission"


@router.get('/get_all_category/', response_model=category_schemas.CategoryResponse)
def get_all_category(page: int, size: int, db: Session = Depends(get_db)):
    return category_repository.get_all_category(db=db, page=page, size=size)


@router.get('/get_category_by_keyword/', response_model=category_schemas.CategoryResponse)
def get_category_by_keyword(page: int, size: int, keyword: Optional[str] = None, db: Session = Depends(get_db)):
    return category_repository.get_category_by_key_word(db, page=page, size=size, keyword=keyword)


@router.put('/update_category/')
def update_category(request: category_schemas.CategoryRequest, id: int, token: Optional[str] = Header(None),
                    db: Session = Depends(get_db)):
    if token is None:
        return "Please login for this action"
    else:
        role: str = validate_user(token=token)
    if role is not None and role == "emp":
        category_repository.update_category(db=db, category=request, id=id)
        return "Category is updated"
    elif role != "emp":
        return "You don't have permission"


@router.delete('/delete_category/')
def delete_category(id: int, token: Optional[str] = Header(None), db: Session = Depends(get_db)):
    if token is None:
        return "Please login for this action"
    else:
        role: str = validate_user(token=token)
    if role is not None and role == "emp":
        category_repository.delete_category(db=db, id=id)
        return "Category is deleted"
    elif role != "emp":
        return "You don't have permission"
