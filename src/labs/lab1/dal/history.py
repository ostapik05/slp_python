from labs.lab1.bll.formatting import get_formatted_float


def add_to_history(calculation, history):
    history.append(calculation)
    return history


def show_history(history, decimals, log_file):
    print("Історія обчислень:")
    if not history:
        print("Історія порожня.")
    else:
        for record in history:
            num1, num2, operator, result = record.values()
            if num2 is not None:
                print(
                    f"{get_formatted_float(num1,decimals, log_file)} {operator} {get_formatted_float(num2,decimals, log_file)} = {get_formatted_float(result,decimals, log_file)}"
                )
            else:
                print(
                    f"{operator}{get_formatted_float(num1,decimals, log_file)} = {get_formatted_float(result,decimals, log_file)}"
                )
