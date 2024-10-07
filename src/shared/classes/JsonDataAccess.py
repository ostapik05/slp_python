from jsonpickle import encode, decode
from json import dumps, loads
from shared.services.FileOperations import *
from shared.classes.FileDataAccess import FileDataAccess, T
from shared.classes.KeyDataAccess import KeyDataAccess
from labs.lab3.dal.AsciiSettingsModel import AsciiSettingsModel


class JsonDataAccess(FileDataAccess[T]):
    def __init__(self, file_path="assets/default.txt"):
        super().__init__(file_path)

    def set(self, data: T):
        json_data = encode(data)
        super().set(json_data)

    def get(self) -> T:
        json_data = super().get()
        return decode(json_data)
