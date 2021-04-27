from sqlalchemy import and_, or_
from sqlalchemy.orm import Session
from app.common.models import Product


def get_all(db: Session):
    products = db.query(Product).all()
    return products


def get_product_by_keyword(db: Session, keyword: str):
    if keyword is not None:
        return db.query(Product).filter(or_(Product.name == keyword,
                                            Product.price == keyword,
                                            Product.id == keyword)).all()
    else:
        return get_all(db)
