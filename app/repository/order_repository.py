from sqlalchemy import and_, or_
from sqlalchemy.orm import Session
from app.common import models
from app.schemas import order_schemas, base_response
from fastapi.encoders import jsonable_encoder