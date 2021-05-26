from sqlalchemy import and_, or_
from sqlalchemy.orm import Session
from app.common import models
from app.schemas import order_schemas, base_response
from fastapi.encoders import jsonable_encoder


def create_order(db: Session, order: order_schemas.OrderRequest):
    db_order = models.Order(create_day=order.create_day,
                            phonenumber=order.phonenumber,
                            andress=order.andress,
                            total_price=order.total_price,
                            status=order.status,
                            description=order.description,
                            customer_id=order.customer_id,
                            employee_id=order.employee_id)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def get_all_order(db: Session, page: int, size: int):
    offset = (page - 1) * size
    res: list = db.query(models.Order).offset(offset).limit(size).all()
    orders: list[order_schemas.Order] = res
    total_record = len(db.query(models.Order).all())
    total_page = int(total_record / size) if total_record % size == 0 else int((total_record / size) + 1)

    result = base_response.BaseResponse(data=orders,
                                        page=page,
                                        size=size,
                                        total_record=total_record,
                                        total_page=total_page)

    response = order_schemas.OrderResponse.from_orm(result)
    return response


def get_order_by_keyword(db: Session, page: int, size: int, keyword: str):
    if keyword is not None:
        offset = (page - 1) * size
        orders: list = db.query(models.Order).join(models.Customer, models.Order.customer_id == models.Customer.id)\
                                             .filter(or_(models.Order.id == keyword,
                                                         models.Customer.lastname+models.Customer.firstname == keyword,
                                                         models.Customer.id == keyword))\
                                             .offset(offset).limit(size).all()

        total_record = len(db.query(models.Order).join(models.Customer, models.Order.customer_id == models.Customer.id)\
                                                 .filter(or_(models.Order.id == keyword,
                                                             models.Customer.lastname+models.Customer.firstname == keyword,
                                                             models.Customer.id == keyword))\
                                                 .offset(offset).limit(size).all())
        total_page = int(total_record / size) if total_record % size == 0 else int((total_record / size) + 1)

        result = base_response.BaseResponse(data=orders,
                                            page=page,
                                            size=size,
                                            total_record=total_record,
                                            total_page=total_page)

        response = order_schemas.OrderResponse.from_orm(result)
        return response
    else:
        return get_all_order(db=db, page=page, size=size)


def update_order(db: Session, order: order_schemas.OrderRequest, id: int):
    if order_is_exists(db=db, id=id) is True:
        update_order_encoded = jsonable_encoder(order)
        res = db.query(models.Order).filter(models.Order.id == id)
        res.update(update_order_encoded)
        db.commit()
        return order
    else:
        return "Not found order id"


def order_is_exists(db: Session, id: int):
    if db.query(models.Order).filter(models.Order.id == id).first() is not None:
        return True
    else:
        return False