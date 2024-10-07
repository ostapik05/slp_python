from typing import Generic, TypeVar

T = TypeVar("T")


class DataAccess(Generic[T]):
    def __init__(self):
        self.data: T = None

    def set(self, data: T):
        self.data = data

    def get(self) -> T:
        return self.data
