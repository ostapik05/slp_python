from init import *
from functions.menu import menu
from classes.Calculator import Calculator


def main():
    # menu(memory, available_operations, decimals, log_file, history)
    calculator = Calculator(
        memory, unary_operations, double_operations, decimals, log_file, history
    )
    calculator.menu()


if __name__ == "__main__":
    main()
