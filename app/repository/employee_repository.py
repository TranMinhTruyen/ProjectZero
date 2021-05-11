from sqlalchemy import and_, or_
from sqlalchemy.orm import Session
from app.common import models
from app.schemas import employee_schemas, base_response
import hashlib
from fastapi.encoders import jsonable_encoder


def create_employee(db: Session, employee: employee_schemas.EmployeeRequest):
    if employee_is_exists(db=db, keyword=employee.account) is False:
        db_employee = models.Employee(account=employee.account,
                                      password=str(hashlib.sha224(employee.password.strip().encode("utf-8")).hexdigest()),
                                      firstname=employee.firstname,
                                      lastname=employee.lastname,
                                      birthday=employee.birthday,
                                      citizen_id=employee.citizen_id,
                                      phonenumber=employee.phonenumber,
                                      andress=employee.andress,
                                      is_active=employee.is_active)
        db.add(db_employee)
        db.commit()
        db.refresh(db_employee)
        return db_employee
    else:
        return None


def get_all_employee(db: Session, page: int, size: int):
    offset = (page - 1) * size
    employees: list = db.query(models.Employee).offset(offset).limit(size).all()
    total_record = len(db.query(models.Employee).all())
    total_page = int(total_record / size) if total_record % size == 0 else int((total_record / size) + 1)
    result = base_response.BaseResponse(data=employees,
                                        page=page,
                                        size=size,
                                        total_record=total_record,
                                        total_page=total_page)

    response = employee_schemas.EmployeeResponse.from_orm(result)
    return response


def get_customer_by_keyword(db: Session, page: int, size: int, keyword: str):
    if keyword is not None:
        offset = (page - 1) * size
        employees: list = db.query(models.Employee).filter(or_(models.Employee.firstname.like(keyword),
                                                               models.Employee.lastname.like(keyword),
                                                               models.Employee.andress.like(keyword),
                                                               models.Employee.account == keyword,
                                                               models.Employee.citizen_id == keyword,
                                                               models.Employee.id == keyword)).offset(offset).limit(
            size).all()
        total_record = len(db.query(models.Employee).filter(or_(models.Employee.firstname.like(keyword),
                                                                models.Employee.lastname.like(keyword),
                                                                models.Employee.andress.like(keyword),
                                                                models.Employee.account == keyword,
                                                                models.Employee.citizen_id == keyword,
                                                                models.Employee.id == keyword)).all())
        total_page = int(total_record / size) if total_record % size == 0 else int((total_record / size) + 1)
        result = base_response.BaseResponse(data=employees,
                                            page=page,
                                            size=size,
                                            total_record=total_record,
                                            total_page=total_page)

        response = employee_schemas.EmployeeResponse.from_orm(result)
        return response
    else:
        return get_all_employee(db=db, page=page, size=size)


def get_employee_by_account_password(db: Session, account: str, password: str):
    return db.query(models.Employee).filter(and_(models.Employee.account == account,
                                                 models.Employee.password == password)).first()


def employee_is_exists(db: Session, keyword: str):
    if db.query(models.Employee).filter(or_(models.Employee.account == keyword,
                                            models.Employee.id == keyword)).first() is not None:
        return True
    else:
        return False


def update_employee(db: Session, employee: employee_schemas.EmployeeRequest, id: int):
    if employee_is_exists(db=db, keyword=id) is True:
        db_employee = models.Employee(account=employee.account,
                                      password=str(
                                          hashlib.sha224(employee.password.strip().encode("utf-8")).hexdigest()),
                                      firstname=employee.firstname,
                                      lastname=employee.lastname,
                                      birthday=employee.birthday,
                                      citizen_id=employee.citizen_id,
                                      phonenumber=employee.phonenumber,
                                      andress=employee.andress,
                                      is_active=employee.is_active)
        update_employee_encoded = jsonable_encoder(db_employee)
        res = db.query(models.Employee).filter(models.Employee.id == id)
        res.update(update_employee_encoded)
        db.commit()
        return db_employee
    else:
        return "Not found employee id"


def delete_employee(db: Session, id: int):
    if employee_is_exists(db=db, keyword=id) is True:
        db.query(models.Employee).filter(models.Employee.id == id).delete(synchronize_session=False)
        db.commit()
        return "Done"
    else:
        return "Not found employee id"
