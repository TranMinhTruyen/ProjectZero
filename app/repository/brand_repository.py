from sqlalchemy import and_, or_
from sqlalchemy.orm import Session
from app.common import models
from app.schemas import brand_schemas, base_response
from fastapi.encoders import jsonable_encoder


def create_brand(db: Session, brand: brand_schemas.BrandRequest):
    if brand_is_exists(db=db, keyword=brand.name) is False:
        db_brand = models.Brand(name=brand.name,
                                image=brand.image,
                                description=brand.description)
        db.add(db_brand)
        db.commit()
        db.refresh(db_brand)
        return db_brand
    else:
        return None


def get_all_brand(db: Session, page: int, size: int):
    offset = (page - 1) * size
    brands: list = db.query(models.Brand).offset(offset).limit(size).all()
    all_page = len(db.query(models.Brand).all())
    total_record = len(brands)
    total_page = int(all_page / size) if all_page % size == 0 else int((all_page / size) + 1)

    result = base_response.BaseResponse(data=brands,
                                        page=page,
                                        size=size,
                                        total_record=total_record,
                                        total_page=total_page)

    response = brand_schemas.BrandResponse.from_orm(result)
    return response


def get_brand_by_key_word(db: Session, page: int, size: int, keyword: str):
    if keyword is not None:
        offset = (page - 1) * size
        brands: list = db.query(models.Brand).filter(or_(models.Brand.name == keyword,
                                                         models.Brand.id == keyword)).offset(offset).limit(size).all()

        all_page = len(db.query(models.Brand).filter(or_(models.Brand.name == keyword,
                                                         models.Brand.id == keyword)).all())
        total_record = len(brands)
        total_page = int(all_page / size) if all_page % size == 0 else int((all_page / size) + 1)

        result = base_response.BaseResponse(data=brands,
                                            page=page,
                                            size=size,
                                            total_record=total_record,
                                            total_page=total_page)

        response = brand_schemas.BrandResponse.from_orm(result)
        return response
    else:
        return get_all_brand(db=db, page=page, size=size)


def brand_is_exists(db: Session, keyword: str):
    if db.query(models.Brand).filter(or_(models.Brand.name == keyword,
                                         models.Brand.id == keyword)).first() is not None:
        return True
    else:
        return False


def update_brand(db: Session, brand: brand_schemas.BrandRequest, id: int):
    if brand_is_exists(db=db, keyword=id) is True:
        update_brand_encoded = jsonable_encoder(brand)
        res = db.query(models.Brand).filter(models.Brand.id == id)
        res.update(update_brand_encoded)
        db.commit()
        return brand
    else:
        return "Not found category id"


def delete_brand(db: Session, id: int):
    if brand_is_exists(db=db, keyword=id) is True:
        db.query(models.Category).filter(models.Category.id == id).delete(synchronize_session=False)
        db.commit()
        return "Done"
    else:
        return "Not found category id"
