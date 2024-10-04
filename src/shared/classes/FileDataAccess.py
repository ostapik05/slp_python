from shared.services.FileOperations import (
    ensure_file_exists,
    write_to_file,
    load_from_file,
)
from shared.classes.DataAccess import DataAccess


class FileDataAccess(DataAccess):
    def __init__(self, file_path="assets/default.txt"):
        ensure_file_exists(file_path)
        self.__file_path = file_path

    def set(self, data):
        write_to_file(data, self.__file_path)

    def get(self):
        return load_from_file(self.__file_path)
