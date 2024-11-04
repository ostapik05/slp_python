from shared.services.FileOperations import (
    ensure_file_exists,
    write_to_file,
    load_from_file,
)
from shared.classes.DataAccess import DataAccess, T


class FileDataAccess(DataAccess):
    def __init__(self, file_path="assets/default.txt", is_caching=False):
        try:
            ensure_file_exists(file_path)
        except Exception as e:
            raise e
        self.__file_path = file_path
        self.is_caching = is_caching
        self.cache = None

    def set_file_path(self, file_path):
        self.__file_path = file_path

    def set(self, data: T):
        if self.is_caching:
            self.cache = data
        try:
            write_to_file(data, self.__file_path)
        except Exception as e:
            raise e

    def get(self) -> T:
        if self.is_caching:
            return self.cache
        try:
            return load_from_file(self.__file_path)
        except Exception as e:
            raise e

    def set_is_caching(self, is_caching):
        if not is_caching:
            self.cache = None
        elif not self.is_caching:
            self.cache = self.get()
        self.is_caching = is_caching
