from typing import Generic, TypeVar, Dict

T = TypeVar("T")


class KeyDataAccess(Generic[T]):
    def __init__(self):
        self.list: Dict[str, T] = {}

    def set(self, key: str, data: T):
        self.list[key] = data

    def get(self, key: str) -> T:
        return self.list[key]
