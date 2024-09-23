from datetime import datetime


def log_error(message, log_file):
    error_message = f"{str(datetime.now())} - {message}"
    print(f"Помилка: {message}")  # Вивід на екран
    write_to_file(error_message, log_file)  # Запис у лог-файл


def write_to_file(message, filepath):
    try:
        with open(filepath, "a", encoding="utf-8") as file:
            file.write(f"{message}\n")
    except Exception as e:
        print(f"Проблема запису у файл: {e}")
