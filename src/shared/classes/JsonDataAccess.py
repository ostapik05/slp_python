from jsonpickle import encode, decode
from shared.services.FileOperations import *
from shared.classes.FileDataAccess import FileDataAccess
from shared.classes.ListDataAccess import ListDataAccess


class JsonDataAccess(ListDataAccess, FileDataAccess):
    def __init__(self, file_path="assets/default.txt"):
        super().__init__(file_path)

    def set(self, data):
        json = encode(data)
        super().set(json)

    def get(self):
        json = super().get()
        return decode(json)
