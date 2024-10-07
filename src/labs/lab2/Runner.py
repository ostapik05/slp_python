from data.lab2.init import *
from labs.lab2.ui.Calculator import Calculator
from shared.interfaces.RunnerInterface import RunnerInterface


class Runner(RunnerInterface):
    @staticmethod
    def run():
        calculator = Calculator(
            memory, unary_operations, double_operations, decimals, log_file
        )
        calculator.menu()


if __name__ == "__main__":
    Runner.run()
