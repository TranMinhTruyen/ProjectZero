from sqlalchemy.orm import Session
from app.common import models


def get_all(db: Session):
    products = db.query(models.Product).all()
    return products