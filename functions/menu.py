from functions.logger import log_error
from functions.memory import *
from functions.history import show_history, add_to_history
from functions.calculator import calculate
from functions.formatting import get_formatted_float


def set_decimals(decimals, log_file):
    try:
        print(f"Кількість знаків після коми: {decimals}")
        decimals = int(input("Введіть нову кількість знаків після коми: "))
        return decimals
    except ValueError:
        log_error("Невірне введення кількості десяткових знаків", log_file)
        return decimals


def is_valid_operator(operator, available_operations, log_file):
    if operator in available_operations:
        return True
    else:
        log_error(f"Невірний оператор: {operator}", log_file)
        return False


def calculation_menu(memory, available_operations, decimals, log_file, history):
    num1, operator, num2 = get_input(memory, available_operations, log_file)
    if is_valid_operator(operator, available_operations, log_file):
        try:
            result = calculate(num1, operator, num2)
            calculation = {
                "num1": num1,
                "num2": num2,
                "operator": operator,
                "result": result,
            }
            history = add_to_history(calculation, history)
            print(f"Результат: {get_formatted_float(result,decimals, log_file)}")
            return memory, history
        except ZeroDivisionError as e:
            log_error(str(e), log_file)
        except ValueError as e:
            log_error(str(e), log_file)
    else:
        log_error(
            f"Неправильний оператор, доступні {', '.join(available_operations)}",
            log_file,
        )
    return memory, history


def get_input(memory, available_operations, log_file):
    try:
        num1_input = input("Введіть перше число або 'mr' для пам'яті: ")
        if num1_input == "mr":
            num1 = memory
        else:
            num1 = float(num1_input)

        operator = input(f"Введіть оператор ({', '.join(available_operations)}): ")

        num2 = None
        if operator != "√" and operator != "sqrt":
            num2_input = input("Введіть друге число або 'mr' для пам'яті: ")
            if num2_input == "mr":
                num2 = memory
            else:
                num2 = float(num2_input)
        return num1, operator, num2
    except ValueError:
        log_error("Неправильне введення", log_file)
        return get_input(memory, available_operations, log_file)


def menu(memory, available_operations, decimals, log_file, history):
    while True:
        print("\n=== Консольний калькулятор ===")
        print(f"M: {get_formatted_float(memory, decimals, log_file)}")
        print("1. Обчислення")
        print("2. Записати результат у пам'ять MS")
        print("3. Додати результат у пам'ять M+")
        print("4. Очистити пам'ять MC")
        print("5. Показати історію обчислень")
        print("6. Налаштувати кількість десяткових знаків")
        print("0. Вийти")
        choice = input("Виберіть опцію (0-5): ")
        match choice:
            case "1":
                memory, history = calculation_menu(
                    memory, available_operations, decimals, log_file, history
                )
            case "2":
                memory = memory_set(memory, history[-1])
            case "3":
                if not history:
                    print("Немає результатів для збереження.")
                    continue
                memory = memory_save(memory, history[-1])

            case "4":
                memory = memory_clean()
            case "5":
                show_history(history, decimals, log_file)
            case "6":
                decimals = set_decimals(decimals, log_file)
            case "0":
                print("Вихід з програми.")
                break
            case _:
                print("Неправильний вибір. Спробуйте ще раз.")
