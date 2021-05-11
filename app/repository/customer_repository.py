from sqlalchemy import and_, or_
from sqlalchemy.orm import Session
from app.common import models
from app.schemas import customer_schemas, base_response
import hashlib
from fastapi.encoders import jsonable_encoder


def create_customer(db: Session, customer: customer_schemas.CustomerRequest):
    if customer_is_exists(db=db, keyword=customer.account) is False:
        db_customer = models.Customer(account=customer.account,
                                      password=str(
                                          hashlib.sha224(customer.password.strip().encode("utf-8")).hexdigest()),
                                      firstname=customer.firstname,
                                      lastname=customer.lastname,
                                      birthday=customer.birthday,
                                      phonenumber=customer.phonenumber,
                                      andress=customer.andress,
                                      is_active=customer.is_active)
        db.add(db_customer)
        db.commit()
        db.refresh(db_customer)
        return db_customer
    else:
        return None


def get_all_customer(db: Session, page: int, size: int):
    offset = (page - 1) * size
    customers: list = db.query(models.Customer).offset(offset).limit(size).all()
    total_record = len(db.query(models.Customer).all())
    total_page = int(total_record / size) if total_record % size == 0 else int((total_record / size) + 1)
    result = base_response.BaseResponse(data=customers,
                                        page=page,
                                        size=size,
                                        total_record=total_record,
                                        total_page=total_page)

    response = customer_schemas.CustomerResponse.from_orm(result)
    return response


def get_customer_by_keyword(db: Session, page: int, size: int, keyword: str):
    if keyword is not None:
        offset = (page - 1) * size
        customers: list = db.query(models.Customer).filter(or_(models.Customer.firstname.like(keyword),
                                                               models.Customer.lastname.like(keyword),
                                                               models.Customer.andress.like(keyword),
                                                               models.Customer.account == keyword,
                                                               models.Customer.id == keyword)).offset(offset).limit(
            size).all()
        total_record = len(db.query(models.Customer).filter(or_(models.Customer.firstname.like(keyword),
                                                                models.Customer.lastname.like(keyword),
                                                                models.Customer.andress.like(keyword),
                                                                models.Customer.account == keyword,
                                                                models.Customer.id == keyword)).all())
        total_page = int(total_record / size) if total_record % size == 0 else int((total_record / size) + 1)
        result = base_response.BaseResponse(data=customers,
                                            page=page,
                                            size=size,
                                            total_record=total_record,
                                            total_page=total_page)

        response = customer_schemas.CustomerResponse.from_orm(result)
        return response
    else:
        return get_all_customer(db=db, page=page, size=size)


def get_customer_by_account_password(db: Session, account: str, password: str):
    return db.query(models.Customer).filter(and_(models.Customer.account == account,
                                                 models.Customer.password == password)).first()


def customer_is_exists(db: Session, keyword: str):
    if db.query(models.Customer).filter(or_(models.Customer.account == keyword,
                                            models.Customer.id == keyword)).first() is not None:
        return True
    else:
        return False


def update_customer(db: Session, customer: customer_schemas.CustomerRequest, id: int):
    if customer_is_exists(db=db, keyword=id) is True:
        db_customer = models.Customer(account=customer.account,
                                      password=str(
                                          hashlib.sha224(customer.password.strip().encode("utf-8")).hexdigest()),
                                      firstname=customer.firstname,
                                      lastname=customer.lastname,
                                      birthday=customer.birthday,
                                      phonenumber=customer.phonenumber,
                                      andress=customer.andress,
                                      is_active=customer.is_active)
        update_customer_encoded = jsonable_encoder(db_customer)
        res = db.query(models.Customer).filter(models.Customer.id == id)
        res.update(update_customer_encoded)
        db.commit()
        return db_customer
    else:
        return "Not found customer id"


def delete_customer(db: Session, id: int):
    if customer_is_exists(db=db, keyword=id) is True:
        db.query(models.Customer).filter(models.Customer.id == id).delete(synchronize_session=False)
        db.commit()
        return "Done"
    else:
        return "Not found customer id"
