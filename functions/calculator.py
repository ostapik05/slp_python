import math


def calculate(num1, operator, num2=None):
    if operator == "+":
        return num1 + num2
    elif operator == "-":
        return num1 - num2
    elif operator == "*":
        return num1 * num2
    elif operator == "/":
        if num2 == 0:
            raise ZeroDivisionError("Ділення на нуль")
        return num1 / num2
    elif operator == "^":
        return num1**num2
    elif operator == "√" or operator == "sqrt":
        if num1 < 0:
            raise ValueError(f"Не можна взяти корінь з від'ємного числа {num1}")
        return math.sqrt(num1)
    elif operator == "%":
        return num1 % num2
