from labs.lab2.bll.Operation import Operation


class History:
    def __init__(self, history):
        self.history = history

    @classmethod
    def empty(self):
        return self(list())

    def add(self, operation: Operation):
        if not isinstance(operation, Operation):
            raise ValueError("Can't add operation to history")
        self.history.append(operation)

    def get(self):
        return self.history

    def clear(self):
        self.history = list()

    def __str__(self) -> str:
        string = "History of calculations:\n"
        if not self.history:
            return string + "History empty.\n"
        for record in self.history:
            if isinstance(record, Operation):
                string += record.__str__() + "\n"

        return string
