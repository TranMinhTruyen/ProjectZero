import hashlib
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
import secrets
from app.common.dependencies import get_db
from sqlalchemy.orm import Session
from app.repository import customer_repository, employee_repository

SECRET_KEY = "mykey"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_password_hash(password: str):
    return str(hashlib.sha224(password.strip().encode("utf-8")).hexdigest())


def authenticate_user(account: str, password: str, db: Session):
    customer = customer_repository.get_customer_by_account_password(account=account,
                                                                    password=get_password_hash(password=password),
                                                                    db=db)
    employee = employee_repository.get_employee_by_account_password(account=account,
                                                                    password=get_password_hash(password=password),
                                                                    db=db)
    if customer is not None:
        return customer
    elif employee is not None:
        return employee
    else:
        return None


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(db: Session, token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        account: str = payload.get("account")
        password: str = payload.get("password")
        if account is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = authenticate_user(account=account, password=password, db=db)
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(current_user: dict = Depends(get_current_user)):
    if current_user.get("is_active") != "active":
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
