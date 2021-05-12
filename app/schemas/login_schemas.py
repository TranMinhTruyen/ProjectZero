from pydantic import BaseModel
from typing import Optional


class LoginRequest(BaseModel):
    account: str
    password: str


class Token(BaseModel):
    token: Optional[str] = None


class Payload(BaseModel):
    account: Optional[str] = None