from typing import List, Generic, TypeVar
from pydantic import BaseModel

T = TypeVar('T')


class BaseResponse:
    def __init__(self, *, data: List, page: int, size: int, total_page: int, total_record: int):
        self.data = data
        self.page = page
        self.size = size
        self.total_page = total_page
        self.total_record = total_record