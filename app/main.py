from typing import Optional

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.router import product
from app.common import models
from app.common.database import engine
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(product.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
## uvicorn app.main:app --reload
