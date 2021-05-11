from sqlalchemy import and_, or_
from sqlalchemy.orm import Session
from app.common import models
from app.schemas import product_schemas, base_response
from fastapi.encoders import jsonable_encoder


def create_product(db: Session, product: product_schemas.ProductRequest):
    if product_is_exists(db=db, keyword=product.name) is False:
        db_product = models.Product(name=product.name,
                                    price=product.price,
                                    unit=product.unit,
                                    in_stock=product.in_stock,
                                    discount=product.discount,
                                    image=product.image,
                                    description=product.description,
                                    category_id=product.category_id,
                                    brand_id=product.brand_id)
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product
    else:
        return "Product is exists"


def get_all_product(db: Session, page: int, size: int):
    offset = (page - 1) * size
    res: list = db.query(models.Product).offset(offset).limit(size).all()
    products: list[product_schemas.Product] = res
    total_record = len(db.query(models.Product).all())
    total_page = int(total_record / size) if total_record % size == 0 else int((total_record / size) + 1)

    result = base_response.BaseResponse(data=products,
                                        page=page,
                                        size=size,
                                        total_record=total_record,
                                        total_page=total_page)

    response = product_schemas.ProductResponse.from_orm(result)
    return response


def get_product_by_keyword(db: Session, page: int, size: int, keyword: str):
    if keyword is not None:
        offset = (page - 1) * size
        products: list = db.query(models.Product).filter(or_(models.Product.name == keyword,
                                                             models.Product.price == keyword,
                                                             models.Product.id == keyword)).offset(offset).limit(
            size).all()
        total_record = len(db.query(models.Product).filter(or_(models.Product.name == keyword,
                                                               models.Product.price == keyword,
                                                               models.Product.id == keyword)).all())
        total_page = int(total_record / size) if total_record % size == 0 else int((total_record / size) + 1)

        result = base_response.BaseResponse(data=products,
                                            page=page,
                                            size=size,
                                            total_record=total_record,
                                            total_page=total_page)

        response = product_schemas.ProductResponse.from_orm(result)
        return response
    else:
        return get_all_product(db=db, page=page, size=size)


def product_is_exists(db: Session, keyword: str):
    if db.query(models.Product).filter(or_(models.Product.name == keyword,
                                           models.Product.id == keyword)).first() is not None:
        return True
    else:
        return False


def update_product(db: Session, product: product_schemas.ProductRequest, id: int):
    if product_is_exists(db=db, keyword=id) is True:
        update_product_encoded = jsonable_encoder(product)
        res = db.query(models.Product).filter(models.Product.id == id)
        res.update(update_product_encoded)
        db.commit()
        return product
    else:
        return "Not found product id"


def delete_product(db: Session, id: int):
    if product_is_exists(db=db, keyword=id) is True:
        db.query(models.Product).filter(models.Product.id == id).delete(synchronize_session=False)
        db.commit()
        return "Done"
    else:
        return "Not found product id"
