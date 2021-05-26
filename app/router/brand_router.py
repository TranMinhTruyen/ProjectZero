from typing import Optional

from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from app.common.dependencies import get_db, validate_user
from app.schemas import brand_schemas
from app.repository import brand_repository

router = APIRouter(
    tags=['Brand'],
    prefix="/brand"
)


@router.post('/create_brand/')
def create_brand(request: brand_schemas.BrandRequest, token: Optional[str] = Header(None), db: Session = Depends(get_db)):
    if token is None:
        return "Please login for this action"
    else:
        role: str = validate_user(token=token)
    if role is not None and role == "emp":
        brand_repository.create_brand(db=db, brand=request)
        return "Brand is added"
    elif role != "emp":
        return "You don't have permission"


@router.get('/get_all_brand/', response_model=brand_schemas.BrandResponse)
def get_all_brand(page: int, size: int, db: Session = Depends(get_db)):
    return brand_repository.get_all_brand(db=db, page=page, size=size)


@router.get('/get_brand_by_keyword/', response_model=brand_schemas.BrandResponse)
def get_brand_by_keyword(page: int, size: int, keyword: Optional[str] = None, db: Session = Depends(get_db)):
    return brand_repository.get_brand_by_key_word(db, page=page, size=size, keyword=keyword)


@router.put('/update_brand/')
def update_brand(request: brand_schemas.BrandRequest, id: int, token: Optional[str] = Header(None), db: Session = Depends(get_db)):
    if token is None:
        return "Please login for this action"
    else:
        role: str = validate_user(token=token)
    if role is not None and role == "emp":
        brand_repository.update_brand(db=db, brand=request, id=id)
        return "Brand is updated"
    elif role != "emp":
        return "You don't have permission"


@router.delete('/delete_brand/')
def delete_brand(id: int, token: Optional[str] = Header(None), db: Session = Depends(get_db)):
    if token is None:
        return "Please login for this action"
    else:
        role: str = validate_user(token=token)
    if role is not None and role == "emp":
        brand_repository.delete_brand(db=db, id=id)
        return "Brand is deleted"
    elif role != "emp":
        return "You don't have permission"
