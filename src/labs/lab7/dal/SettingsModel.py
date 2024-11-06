from shared.classes.DictJsonDataAccess import DictJsonDataAccess
from shared.services.FileOperations import ensure_file_exists


class SettingsModel:
    def __init__(self, path):
        self.__settings = DictJsonDataAccess(path)
        if not self.__settings.validate(is_can_be_empty=False):
            raise KeyError("Settings empty or doesn't exist")

    def get_fields(self):
        return self.__settings.get('fields')

    def get_fields_keys(self):
        keys = list(self.get_fields().keys())
        return keys

    def get_user_settings_path(self):
        return self.__settings.get('user_settings_path')

    def get_history_path(self):
        return self.__settings.get('history_path')

    def get_languages(self):
        return self.__settings.get('languages')

    def get_max_results(self):
        return self.__settings.get('max_results')

    def get_default_save_dir(self):
        return self.__settings.get('default_save_dir')

    def get_default_file_name(self):
        return self.__settings.get('default_file_name')

    def get_results_to_save(self):
        return self.__settings.get('results_to_save')

    def get_colors(self):
        return self.__settings.get('colors')

    def get_attributes(self):
        return self.__settings.get('attributes')
