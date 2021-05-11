from sqlalchemy import and_, or_
from sqlalchemy.orm import Session
from app.common import models
from app.schemas import category_schemas, base_response
from fastapi.encoders import jsonable_encoder


def create_category(db: Session, category: category_schemas.CategoryRequest):
    if category_is_exists(db=db, keyword=category.name) is False:
        db_category = models.Category(name=category.name,
                                      description=category.description)
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category
    else:
        return "Category is exists"


def get_all_category(db: Session, page: int, size: int):
    offset = (page - 1) * size
    categories: list = db.query(models.Category).offset(offset).limit(size).all()
    total_record = len(db.query(models.Category).all())
    total_page = int(total_record / size) if total_record % size == 0 else int((total_record / size) + 1)

    result = base_response.BaseResponse(data=categories,
                                        page=page,
                                        size=size,
                                        total_record=total_record,
                                        total_page=total_page)

    response = category_schemas.CategoryResponse.from_orm(result)
    return response


def get_category_by_key_word(db: Session, page: int, size: int, keyword: str):
    if keyword is not None:
        offset = (page - 1) * size
        categories: list = db.query(models.Category).filter(or_(models.Category.name == keyword,
                                                                models.Category.id == keyword)).offset(offset).limit(
            size).all()

        total_record = len(db.query(models.Category).filter(or_(models.Category.name == keyword,
                                                                models.Category.id == keyword)).all())
        total_page = int(total_record / size) if total_record % size == 0 else int((total_record / size) + 1)

        result = base_response.BaseResponse(data=categories,
                                            page=page,
                                            size=size,
                                            total_record=total_record,
                                            total_page=total_page)

        response = category_schemas.CategoryResponse.from_orm(result)
        return response
    else:
        return get_all_category(db=db, page=page, size=size)


def category_is_exists(db: Session, keyword: str):
    if db.query(models.Category).filter(or_(models.Category.name == keyword,
                                            models.Category.id == keyword)).first() is not None:
        return True
    else:
        return False


def update_category(db: Session, category: category_schemas.CategoryRequest, id: int):
    if category_is_exists(db=db, keyword=id) is True:
        update_category_encoded = jsonable_encoder(category)
        res = db.query(models.Category).filter(models.Category.id == id)
        res.update(update_category_encoded)
        db.commit()
        return category
    else:
        return "Not found category id"


def delete_category(db: Session, id: int):
    if category_is_exists(db=db, keyword=id) is True:
        db.query(models.Category).filter(models.Category.id == id).delete(synchronize_session=False)
        db.commit()
        return "Done"
    else:
        return "Not found category id"
