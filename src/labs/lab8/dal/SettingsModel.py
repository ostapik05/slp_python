from shared.classes.DictJsonDataAccess import DictJsonDataAccess
import logging
logger = logging.getLogger(__name__)

class SettingsModel:
    def __init__(self, path):
        self.__settings = DictJsonDataAccess(path)
        if not self.__settings.validate(is_can_be_empty=False):
            raise KeyError("Settings empty or doesn't exist")

    def get_assets_save_dir(self):
        return self.__settings.get('assets_save_dir')

    def get_activity_file_path(self):
        return self.__settings.get('activity_file_path')

    def get_sleep_file_path(self):
        return self.__settings.get('sleep_file_path')

    def get_default_file_name(self):
        return self.__settings.get('default_file_name')

    def get_logger_path(self):
        return self.__settings.get('logger_path')
