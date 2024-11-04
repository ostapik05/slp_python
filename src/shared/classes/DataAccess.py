from typing import Generic, TypeVar

T = TypeVar("T")

class DataAccess:
    def __init__(self):
        self.data: T = None

    def set(self, data: T):
        self.data = data

    def get(self) -> T:
        return self.data
