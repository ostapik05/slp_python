from shared.classes.DictJsonDataAccess import DictJsonDataAccess
from shared.services.relative_to_absolute_path import absolute
import logging
logger = logging.getLogger(__name__)

class UserSettingsModel:
    def __init__(self, path):
        self.__settings = DictJsonDataAccess(path)
        if not self.__settings.validate(is_can_be_empty=False):
            logger.critical("There no user settings file")
            raise KeyError("Settings doesn't exist")

    def get_selected_fields(self):
        return self.__settings.get("selected_fields")

    def get_table_fields(self):
        selected_fields = self.get_selected_fields()
        return selected_fields.get('table')

    def set_table_fields(self, table_fields):
        selected_fields = self.get_selected_fields()
        selected_fields['table'] = table_fields
        self.__settings.set("selected_fields", selected_fields)

    def get_list_fields(self):
        selected_fields = self.get_selected_fields()
        return selected_fields.get('list')

    def set_list_fields(self, list_fields):
        selected_fields = self.get_selected_fields()
        selected_fields['list'] = list_fields
        self.__settings.set("selected_fields", selected_fields)

    def get_is_table_print(self):
        return self.__settings.get("is_table_print")

    def set_is_table_print(self, is_table_print):
        self.__settings.set("is_table_print", is_table_print)

    def get_is_list_print(self):
        return self.__settings.get("is_list_print")

    def set_is_list_print(self, is_list_print):
        self.__settings.set("is_list_print", is_list_print)

    def get_lang(self):
        return self.__settings.get("lang")

    def set_lang(self, lang):
        self.__settings.set("lang", lang)

    def get_items_amount(self):
        return self.__settings.get("items_amount")

    def set_items_amount(self, max_results):
        self.__settings.set("items_amount", max_results)

    def get_field_styles(self):
        return self.__settings.get("field_styles")



