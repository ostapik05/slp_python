from os.path import exists, dirname
from os import makedirs


def ensure_file_exists(file_path):
    try:
        if exists(file_path):
            return
        makedirs(dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            return
    except PermissionError as e:
        raise e(f"Can't create file, not enough permitions: {e}")
    except OSError as e:
        raise e(f"Error occurred while creating the file or directories: {e}")
    except Exception as e:
        raise e(f"Error occurred while creating the file or directories: {e}")


def write_to_file(data, file_path):
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(data)
    except Exception as e:
        raise e(f"Error occurred while writing the file: {e}")


def load_from_file(file_path):
    try:
        with open(file_path, "r") as file:
            data = file.read()
        return data
    except FileNotFoundError as e:
        raise e(f"Can't load from file, file not found: {e}")
    except Exception as e:
        raise e(f"Can't load from file: {e}")
