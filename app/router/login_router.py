from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import APIKeyCookie
from app.common.dependencies import get_db, create_access_token, authenticate_user, timedelta, decode_access_token, \
    get_password_hash
from app.repository import customer_repository, employee_repository
from app.schemas import login_schemas, customer_schemas

router = APIRouter(
    tags=['Login'],
    prefix="/login"
)

ACCESS_TOKEN_EXPIRE_MINUTES = 30
cookie_sec = APIKeyCookie


@router.post("/get_access_token")
async def login_for_access_token(request: login_schemas.LoginRequest,
                                 db: Session = Depends(get_db)):
    user = authenticate_user(db=db, account=request.account, password=request.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "account": request.account,
            "password": request.password,
            "role": user.get("role")
        },
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/get_info")
async def get_info(token: login_schemas.Token, db=Depends(get_db)):
    payload: dict = decode_access_token(token=token.token)
    account: str = payload.get("account")
    password: str = payload.get("password")
    role: str = payload.get("role")
    if role == "user":
        return customer_repository.get_customer_by_account_password(db=db,
                                                                    account=account,
                                                                    password=get_password_hash(password))
    else:
        return employee_repository.get_employee_by_account_password(db=db,
                                                                    account=account,
                                                                    password=get_password_hash(password))