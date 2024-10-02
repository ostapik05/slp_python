class Operation:
    def __init__(self, operation, num1, num2=None, result=None):
        self.operation = operation
        self.num1 = num1
        self.num2 = num2
        self.result = result

    @classmethod
    def unary(self, operation, num1, result):
        return self(operation, num1, None, result)

    @classmethod
    def double(self, operation, num1, num2, result):
        return self(operation, num1, num2, result)

    @classmethod
    def empty(self):
        return self(None, None, None, None)

    def __str__(self):
        if self.result is None:
            result = ""
        else:
            result = f" = {self.result}"
        if self.num2 is None:
            return f"{self.operation}{self.num1}{result}"
        else:
            return f"{self.num1} {self.operation} {self.num2}{result}"

    def is_complete(self):
        if self.result == None:
            return False
        else:
            return True

    def set_result(self, result):
        self.result = result

    def get_result(self):
        return self.result

    def to_components(self):
        return self.operation, self.num1, self.num2, self.result

    def get_operator(self):
        return self.operation

    def get_first_number(self):
        return self.num1

    def get_second_number(self):
        return self.num2
