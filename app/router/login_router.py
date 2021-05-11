from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.common.dependencies import get_db
from app.authenticate import login_dependency
from app.schemas import login_schemas

router = APIRouter(
    tags=['Login'],
    prefix="/login"
)


@router.post("/token")
async def login_for_access_token(request: login_schemas.LoginRequest, db: Session = Depends(get_db)):
    user = login_dependency.authenticate_user(db=db, account=request.account, password=request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = login_dependency.timedelta(minutes=login_dependency.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = login_dependency.create_access_token(
        data={"account": request.account,
              "password": request.password}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/users/me/")
async def read_users_me(token: str, db: Session = Depends(get_db)):
    return login_dependency.get_current_user(db=db, token=token)
