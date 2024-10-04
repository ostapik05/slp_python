class ListDataAccess:
    def __init__(self):
        self.list = {}

    def set(self, key, data):
        self.list[key] = data

    def get(self, key):
        return self.list[key]
