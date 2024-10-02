from datetime import datetime
from os.path import exists, dirname
from os import makedirs


# In creation, if file don't exists
# raise error
class Logger:
    # Log to file and to console if needed
    def __init__(self, file_path=None, is_write_to_console=True):

        if not file_path is None:
            self._ensure_file_exists(file_path)
            self.is_write_to_file = False
        else:
            self.file_path = file_path
            self.is_write_to_file = True
        self.is_write_to_console = is_write_to_console

    @classmethod
    def console_only(self):
        return self()

    @classmethod
    def file_only(self, file_path):
        return self(file_path, False)

    @classmethod
    def console_and_file(self, file_path):
        return self(file_path)

    def log_error(self, message, error_level="ERROR"):
        error_message = f"{str(datetime.now())} - {message}"
        if self.is_write_to_console:
            print(f"{error_level}: {message}")
        if self.is_write_to_file:
            self._write_to_file(error_message)

    def _ensure_file_exists(self, file_path):
        try:
            if exists(file_path):
                return
            makedirs(dirname(file_path), exist_ok=True)
            with open(file_path, "w") as file:
                return
        except (OSError, PermissionError) as e:
            raise f"Error occurred while creating the file or directories: {e}"

    def _write_to_file(self, message):
        try:
            with open(self.file_path, "a", encoding="utf-8") as file:
                file.write(f"{message}\n")
        except Exception as e:
            print(f"Problem writing to file: {e}")
