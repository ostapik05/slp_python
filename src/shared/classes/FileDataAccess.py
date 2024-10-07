from shared.services.FileOperations import (
    ensure_file_exists,
    write_to_file,
    load_from_file,
)
from shared.classes.DataAccess import DataAccess, T


class FileDataAccess(DataAccess[T]):
    def __init__(self, file_path="assets/default.txt", is_caching=True):
        try:
            ensure_file_exists(file_path)
        except Exception as e:
            raise e
        self.__file_path = file_path
        self.is_caching = is_caching
        self.cache = None

    def set(self, data: T):
        if self.is_caching:
            self.cache = data
        try:
            write_to_file(data, self.__file_path)
        except Exception as e:
            raise e

    def get(self) -> T:
        if self.is_caching and self.cache:
            return self.cache
        try:
            return load_from_file(self.__file_path)
        except Exception as e:
            raise e

    def set_caching(self, is_caching):
        self.is_caching = is_caching
