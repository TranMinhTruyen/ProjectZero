from typing import List


class CommonResponse:
    page: int
    size: int
    data: List

    def __init__(self, *, page: int, size: int, data: List):
        self.page = page
        self.size = size
        self.data = data
