import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.router import product_router, category_router, brand_router, customer_router, employee_router, login_router
from app.common import models
from app.common.database import engine
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(product_router.router)
app.include_router(category_router.router)
app.include_router(brand_router.router)
app.include_router(customer_router.router)
app.include_router(employee_router.router)
app.include_router(login_router.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Swagger URL: http://127.0.0.1:8000/docs#/
# Start Server: uvicorn app.main:app --reload

if __name__ == "__main__":
    uvicorn.run(app)
