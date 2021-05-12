from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from app.common.dependencies import get_db, create_access_token, authenticate_user, timedelta
from app.schemas import login_schemas

router = APIRouter(
    tags=['Login'],
    prefix="/login"
)

ACCESS_TOKEN_EXPIRE_MINUTES = 30


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
        data={"account": request.account,
              "password": request.password}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
