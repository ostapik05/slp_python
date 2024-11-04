from jsonpickle import encode, decode
from shared.classes.FileDataAccess import FileDataAccess, T


class JsonDataAccess(FileDataAccess):
    def __init__(self, file_path="config/app_settings/default.txt", is_caching=True):
        self.cache = None
        self.is_caching = is_caching
        super().__init__(file_path,False)

    def set(self, data: T):
        if self.is_caching:
            self.cache = data
        json_data = encode(data)
        super().set(json_data)

    def get(self) -> T:
        if self.is_caching:
            return self.cache
        json_data = super().get()
        return decode(json_data)

    def set_is_caching(self, is_caching):
        if not is_caching:
            self.cache = None
        elif not self.is_caching:
            self.cache = self.get()
        self.is_caching = is_caching
