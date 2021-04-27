from sqlalchemy.orm import Session

from app.repository import product_repository
from app.schemas.common_response import CommonResponse


def get_product_by_keyword(db: Session, page: int, size: int, keyword: str):
    result: list = product_repository.get_product_by_keyword(db, keyword=keyword)
    response = CommonResponse(page=page, size=len(result), data=result)
    return response
