from classes.Memory import Memory
from classes.Logger import Logger
from math import sqrt


class Calculator:
    def __init__(
        self,
        memory_value,
        unary_operations,
        double_operations,
        decimals,
        log_file,
        history,
    ):
        self.num1 = None
        self.num2 = None
        self.operator = None
        self.result = None
        self.unary_operations = unary_operations
        self.double_operations = double_operations
        self.decimals = decimals
        self.history = history
        self.memory = Memory(memory_value)
        # If can't write to file than logs to console
        try:
            self.logger = Logger(log_file)
        except Exception as e:
            print(f"{e} \nErrors only in console now")
            self.logger = Logger()

    def is_operator_valid(self, operator):
        if operator in self.unary_operations:
            return True
        elif operator in self.double_operations:
            return True
        else:
            return False

    @staticmethod
    def is_numeric_var(var):
        try:
            float(var)
            return True
        except:
            return False

    def is_setted_operator_valid(self):
        return self.is_valid_operator(self.operator)

    def is_setted_nums_valid(self, is_first_to_check=True, is_second_to_check=True):
        try:
            if is_first_to_check:
                self.is_numeric_var(self.num1)
            if is_second_to_check:
                self.is_numeric_var(self.num2)
            return True
        except:
            return False

    def is_operator_and_num_valid(self):
        if self.operator in self.unary_operations:
            return self.is_setted_nums_valid(True, False)
        elif self.operator in self.double_operations:
            return self.is_setted_nums_valid(True, True)
        else:
            return False

    def set_decimals(self):
        try:
            print(f"Decimals now: {self.decimals}")
            decimals = int(input("Input new amound of decimals: "))
            return decimals
        except ValueError:
            print("It's not a integer, try again")
            self.set_decimals()

    def set_operation(self):
        try:
            num1_input = input("Enter first number or 'mr' for take from memory: ")
            if num1_input == "mr":
                self.num1 = self.memory.get()
            else:
                self.num1 = self.is_numeric_var(num1_input)
            self.operator = input(
                f"Введіть оператор ({', '.join(self.available_operations)}): "
            )
            if self.operator in self.double_operations:
                num2_input = input("Enter second number or 'mr' for take from memory: ")
                if num2_input == "mr":
                    self.num2 = self.memory.get()
                else:
                    self.num2 = self.is_numeric_var(num2_input)

            if not self.is_operator_and_num_valid():
                raise ValueError()
        except ValueError as e:
            print(
                f"Wrong input in operation setting num1:{self.num1} num2: {self.num2} operation: {self.operation}"
            )
            return self.set_operation(self)

    def calculate(self):
        if not self.is_operator_and_num_valid():
            raise ValueError(
                "Wrong input in operation setting num1:{self.num1} num2: {self.num2} operation: {self.operation}"
            )
        if self.operator == "+":
            self.result = self.num1 + self.num2
        elif self.operator == "-":
            self.result = self.num1 - self.num2
        elif self.operator == "*":
            self.result = self.num1 * self.num2
        elif self.operator == "/":
            if self.num2 == 0:
                raise ZeroDivisionError("Division by zero")
            self.result = self.num1 / self.num2
        elif self.operator == "^":
            return self.num1**self.num2
        elif self.operator == "√" or self.operator == "sqrt":
            if self.num1 < 0:
                raise ValueError(
                    f"Can't take square root from negative number {self.num1}"
                )
            return sqrt(self.num1)
        elif self.operator == "%":
            if self.num2 == 0:
                raise ZeroDivisionError("Division by zero")
            return self.num1 % self.num2

    def equation_to_str(self, num1, num2, operation, result):
        is_unary = operation in self.unary_operations
        is_double = operation in self.double_operations
        is_first_num = self.is_numeric_var(num1)
        is_second_num = self.is_numeric_var(num2)
        if is_unary and is_first_num:
            return f"{operation}{num1} = {result}"
        elif is_double and is_second_num:
            return f"{num1} {operation} {num2} = {result}"
        else:
            self.logger.log_error(
                f"Wrong inputs in equation_to_str: num1: {num1}, num2: {num2}, operation: {operation}, result: {result}"
            )
            return ""

    def show_history(self):
        print("History of calculations:")
        if not self.history:
            print("History empty.")
        else:
            for record in self.history:
                num1, num2, operator, result = record.values()
                if operator in self.unary_operations:
                    print(
                        f"{operator}{self.get_formatted_float(num1)} = {self.get_formatted_float(result)}"
                    )
                else:
                    print(
                        f"{self.get_formatted_float(num1)} {operator} {self.get_formatted_float(num2)} = {self.get_formatted_float(result)}"
                    )

    def add_last_to_history(self):
        is_unary = self.operation in self.unary_operations
        is_double = self.operation in self.double_operations
        is_first_num = self.is_numeric_var(self.num1)
        is_second_num = self.is_numeric_var(self.num2)
        calculation = {
            "num1": self.num1,
            "num2": None,
            "operator": self.operator,
            "result": self.result,
        }
        if is_unary and is_first_num:
            calculation["num2"] = None
            self.history.append(calculation)
        elif is_double and is_second_num:
            self.history.append(calculation)
        else:
            self.logger.log_error(
                f"Wrong state of object, can't add to history: num1: {self.num1}, num2: {self.num2}, operation: {self.operation}, result: {self.result}"
            )
            return ""

    def last_result_to_str(self):
        return self.equation_to_str(self.num1, self.num2, self.operator, self.result)

    def get_formatted_float(self, value):
        try:
            new_value = self.is_numeric_var(value)
            format_template = "{0:." + str(self.decimals) + "f}"
            return format_template.format(value)
        except ValueError as e:
            self.logger.log_error(f"Can't format {value} into float, {e}")
            return value

    def menu(self):
        while True:
            formatted_memory = self.get_formatted_float(self.memory.get())
            print("\n=== Console calculator ===")
            print(f"M: {formatted_memory}")
            print("1. Calculation")
            print("2. Wrote result in memory MS")
            print("3. Add result to memory M+")
            print("4. Set memory to 0 MC")
            print("5. Show calculation history")
            print("6. Set how much decimals to show")
            print("0. Exit")
            choice = input("Choose (0-5): ")
            match choice:
                case "1":
                    self.set_operation()
                    self.calculate()
                    self.add_last_to_history()
                    print(self.last_result_to_str())
                case "2":
                    if self.result == None:
                        print("No available results")
                        continue
                    self.memory.set(self.result)
                case "3":
                    if self.result == None:
                        print("No available results")
                        continue
                    self.memory.add(self.result)
                case "4":
                    self.memory.clear()
                case "5":
                    self.show_history()
                case "6":
                    self.set_decimals()
                case "0":
                    print("Exit.")
                    break
                case _:
                    print("Wrong choise, try again.")
