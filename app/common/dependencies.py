import hashlib
from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, status, Depends
from jose import jwt, JWTError
from app.repository import customer_repository, employee_repository
from sqlalchemy.orm import Session
from app.common.database import SessionLocal
import secrets

SECRET_KEY = secrets.token_hex(64)
ALGORITHM = "HS256"



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(claims=to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        account: str = payload.get("account")
        password: str = payload.get("password")
        role: str = payload.get("role")
        if account is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return {"account": account,
            "password": password,
            "role": role}


def get_password_hash(password: str):
    return str(hashlib.sha224(password.strip().encode("utf-8")).hexdigest())


def validate_user(token: str):
    payload: dict = decode_access_token(token=token)
    role: str = payload.get("role")
    if payload is not None and role == "user":
        return "user"
    elif payload is not None and role == "emp":
        return "emp"
    else:
        return None


def authenticate_user(account: str, password: str, db: Session):
    customer = customer_repository.get_customer_by_account_password(account=account,
                                                                    password=get_password_hash(password=password),
                                                                    db=db)
    employee = employee_repository.get_employee_by_account_password(account=account,
                                                                    password=get_password_hash(password=password),
                                                                    db=db)
    if customer is not None:
        return {"customer": customer,
                "role": "user"}
    elif employee is not None:
        return {"employee": employee,
                "role": "emp"}
    else:
        return None
