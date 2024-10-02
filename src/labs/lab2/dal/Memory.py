class Memory:
    def __init__(self, init_value=0.0) -> None:
        self.memory = init_value

    def set(self, value):
        self.memory = value
        return self.memory

    def add(self, value):
        self.memory += value
        return self.memory

    def get(self):
        return self.memory

    def clear(self):
        self.memory = 0.0
        return self.memory
