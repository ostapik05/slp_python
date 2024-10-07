from labs.lab2.dal.Memory import Memory
from labs.lab2.dal.Logger import Logger
from labs.lab2.bll.Validator import Validator
from labs.lab2.bll.Operation import Operation
from labs.lab2.dal.History import History
from math import sqrt


class Calculator:
    def __init__(
        self,
        memory_value,
        unary_operations,
        double_operations,
        decimals,
        log_file,
    ):
        self.unary_operations = unary_operations
        self.double_operations = double_operations
        self.decimals = decimals
        self.history = History.empty()
        self.operation = Operation.empty()
        self.validator = Validator(unary_operations, double_operations)
        self.memory = Memory(memory_value)
        # If can't write to file than logs to console
        try:
            self.logger = Logger.console_and_file(log_file)
        except Exception as e:
            print(f"{e} \nErrors only in console now")
            self.logger = Logger.console_only()

    def is_setted_operator_valid(self):
        return self.validator.is_operator(self.operator)

    def set_decimals(self):
        try:
            print(f"Decimals now: {self.decimals}")
            decimals = int(input("Input new amound of decimals: "))
            self.decimals = decimals
        except ValueError:
            print("It's not a integer, try again")
            self.set_decimals()

    def set_operation(self):
        try:
            num1_input = input("Enter first number or 'mr' for take from memory: ")
            if num1_input == "mr":
                num1 = self.memory.get()
            else:
                num1 = self.validator.to_float(num1_input)

            if not self.validator.is_numeric(num1):
                raise ValueError(f"Wrong first number {num1}")
            operator = input(
                f"Input operator ({self.validator.available_operators_str()}): "
            )
            if not self.validator.is_operator(operator):
                raise ValueError("Wrong operator")
            if self.validator.is_double(operator):
                num2_input = input("Enter second number or 'mr' for take from memory: ")
                if num2_input == "mr":
                    num2 = self.memory.get()
                else:
                    num2 = self.validator.to_float(num2_input)
                if not self.validator.to_float(
                    num2
                ) != 0.0 or not self.validator.to_float(num2):
                    raise ValueError(f"Wrong second number {num2}")
            else:
                num2 = None
            operation = Operation(operator, num1, num2)
            self.operation = operation
        except ValueError as e:
            print(f"Wrong input. {e}")
            return self.set_operation()

    def _calculate(self):
        try:
            operation = self.operation
            operator = operation.get_operator()
            num1 = operation.get_first_number()
            num2 = operation.get_second_number()
            if not self.validator.is_equasion_incomplete(operation):
                raise ValueError(
                    f"Wrong equasion, can't _calculate num1:{num1} num2: {num2} operator: {operator}"
                )
            match operator:
                case "+":
                    operation.set_result(num1 + num2)
                case "-":
                    operation.set_result(num1 - num2)
                case "*":
                    operation.set_result(num1 * num2)
                case "/":
                    if operation.num2 == 0:
                        raise ZeroDivisionError("Division by zero")
                    operation.set_result(num1 / num2)
                case "^":
                    operation.set_result(num1**num2)
                case "√" | "sqrt":
                    if num1 < 0:
                        raise ValueError(f"Can't take square root from {num1}")
                    else:
                        operation.set_result(sqrt(num1))
                case "%":
                    if num2 == 0:
                        operation.set_result(num1 % num2)
                case _:
                    raise ValueError(f"Wrong operator{operator}")
        except Exception as e:
            self.logger.log_error(e)
            raise e

    def _add_last_to_history(self):
        operation = self.operation
        if not self.validator.is_equasion_complete(operation):
            self.logger.log_error(f"Can't add to history {operation}, wrong")
        if not self.operation.is_complete():
            self.logger.log_error(f"Can't add to history {operation}, incomplete")
        self.history.add(operation)

    def _last_result_to_str(self):
        return self.operation.to_string(self.decimals)

    def get_formatted_float(self, value):
        try:
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
            choice = input("Choose (0-6): ")
            match choice:
                case "1":
                    try:
                        self.set_operation()
                        self._calculate()
                        self._add_last_to_history()
                        print(self._last_result_to_str())
                    except Exception as e:
                        self.logger.log_error(e)
                        continue
                case "2":
                    last_result = self.operation.get_result()
                    if last_result == None:
                        print("No available results")
                        continue
                    self.memory.set(last_result)
                case "3":
                    last_result = self.operation.get_result()
                    if last_result == None:
                        print("No available results")
                        continue
                    self.memory.add(last_result)
                case "4":
                    self.memory.clear()
                case "5":
                    print(self.history.to_string(self.decimals))
                case "6":
                    self.set_decimals()
                case "0":
                    print("Exit.")
                    break
                case _:
                    print("Wrong choise, try again.")
