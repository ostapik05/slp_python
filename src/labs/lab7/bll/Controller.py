from os.path import join

from requests import HTTPError

from labs.lab7.bll.ItemExtraction import extract_data_items
from labs.lab7.bll.GoogleBooksAPI import GoogleBooksAPI
from labs.lab7.bll.InputParser import InputParser
from labs.lab7.dal.FileHandler import FileHandler
from labs.lab7.dal.SettingsModel import SettingsModel
from labs.lab7.dal.HistoryModel import HistoryModel
from labs.lab7.dal.UserSettingsModel import UserSettingsModel
from shared.services.relative_to_absolute_path import absolute


class Controller:
    def __init__(self, settings: SettingsModel, history: HistoryModel, user_settings: UserSettingsModel,
                 api: GoogleBooksAPI):
        self.settings = settings
        self.history = history
        self.user_settings = user_settings
        self.api = api
        self.last_query = "Testing"
        self.last_regex = '^195[5-9]|^19[6-9]'
        self.regex_field_name = "Publishing date"


    def set_last_query(self, query):
        self.last_query = query

    def set_last_regex(self, regex):
        self.last_regex = regex

    def set_regex_field_name(self, field):
        self.regex_field_name = field

    def clean_regex_field_name(self):
        self.last_regex = None
        self.regex_field_name = None

    # ^201[8-9]|202
    # ^201[7-9]|202

    @staticmethod
    def is_regex(query):
        return InputParser.is_regex(query)

    @staticmethod
    def parse_query(data, field, query):
        is_wrapped = hasattr(data, "items") and field.startswith("items.")
        if is_wrapped:
            data = data["items"]
            field = field.replace("items.", "", 1)
        new_data = InputParser.parse_query(data, field, query)
        if is_wrapped:
            new_data = {"items": new_data}
        return new_data


    def search_for_table(self):
        if not self.get_is_table():
            return None
        table_fields = self.user_settings.get_table_fields()
        return self.search(table_fields), table_fields

    def search_for_list(self):
        if not self.get_is_list():
            return None
        list_fields = self.user_settings.get_list_fields()
        return self.search(list_fields), list_fields

    def search(self, fields_names=None):
        query = self.last_query
        if not query:
            return None
        if self.regex_field_name:
            fields_names.append(self.regex_field_name)
        lang = self.user_settings.get_lang()
        max_results = self.settings.get_max_results()
        items_amount = self.user_settings.get_items_amount()
        fields = self.names_to_fields(fields_names)
        items = []
        start_index = 0
        total_items = None

        while len(items) < items_amount and (total_items is None or start_index < total_items):
            is_total_items = True if total_items is None else False
            response, total_items = self._fetch_additional_results(
                query, lang, start_index, max_results, fields, is_total_items
            )
            current_batch_results = response
            items.extend(current_batch_results)
            start_index += max_results
            if len(items) >= items_amount:
                break
        result = {"items": items[:items_amount]}
        self.add_to_history(query, self.last_regex, self.regex_field_name, fields_names, result)
        return result

    def add_to_history(self, query, regex, regex_field_name, fields_names, results):
        self.history.add(query, regex, regex_field_name, fields_names, results)

    def _fetch_additional_results(self, query, lang, start_index, max_results, fields, is_total_items=False):
        try:
            temp_result, url = self.api.search(query, lang, start_index, max_results, fields)
            temp_result = self._apply_regex_if_needed(temp_result)
            total_items = temp_result.get("totalItems") if is_total_items else None
            return temp_result["items"], total_items
        except HTTPError as e:
            raise Exception(f"Bad API response: {e}") from e
        except Exception as e:
            raise Exception(str(e)) from e

    def _apply_regex_if_needed(self, data):
        return self.do_regex(data) if self.last_regex and self.regex_field_name else data

    def name_to_field(self, field_name, fields_dict=None):
        if not fields_dict:
            fields_dict = self.settings.get_fields()
        return fields_dict.get(field_name)

    def names_to_fields(self, fields_names):
        fields = []
        if fields_names is None:
            return fields
        fields_dict = self.settings.get_fields()
        for name in fields_names:
            field = self.name_to_field(name, fields_dict)
            if field:
                fields.append(field)
        return fields

    def do_regex(self, data):
        regex = self.last_regex
        field = self.name_to_field(self.regex_field_name)
        if not regex or not field:
            raise ValueError("No regex and field to do regex")
        result = self.parse_query(data, field, regex)
        return result

    def get_regex_field_name(self):
        return self.regex_field_name

    def get_regex(self):
        return self.last_regex

    def get_query(self):
        return self.last_query

    def get_selected_fields(self, mode):
        if mode == "List":
            fields = self.user_settings.get_list_fields()
        elif mode == "Table":
            fields = self.user_settings.get_table_fields()
        else:
            raise ValueError("Wrong mode")
        return fields

    def set_selected(self, chosen_fields, mode="List"):
        if mode == "List":
            self.user_settings.set_list_fields(chosen_fields)
        elif mode == "Table":
            self.user_settings.set_table_fields(chosen_fields)
        else:
            raise ValueError("Wrong mode")

    def set_is_list(self, is_list):
        self.user_settings.set_is_list_print(is_list)

    def set_is_table(self, is_table):
        self.user_settings.set_is_table_print(is_table)

    def get_is_list(self):
        return self.user_settings.get_is_list_print()

    def get_is_table(self):
        return self.user_settings.get_is_table_print()

    def get_fields(self):
        return self.settings.get_fields()

    def get_fields_keys(self):
        return self.settings.get_fields_keys()

    def get_history(self):
        return self.history.get_history()

    def clear_history(self):
        self.history.clear_history()

    def get_languages(self):
        return self.settings.get_languages()

    def get_max_results(self):
        return self.settings.get_max_results()

    def _get_default_save_dir(self):
        return self.settings.get_default_save_dir()

    def get_default_save_dir(self):
        save_path = self._get_default_save_dir()
        path = absolute(save_path)
        return path

    def get_default_file_name(self):
        return self.settings.get_default_file_name()
        
    def get_field_styles(self):
        return self.user_settings.get_field_styles()

    def flat_search(self, mode = "List"):
        if mode == "List":
            data, selected_fields = self.search_for_list()
        elif mode == "Table":
            data, selected_fields = self.search_for_table()
        else:
            raise ValueError("Wrong mode")
        fields_dict = self.settings.get_fields()
        extracted_items = extract_data_items(data, selected_fields, fields_dict)
        return extracted_items, selected_fields

    def save_to_json(self,file_path):
        result = {}
        if self.get_is_table():
            data = self.search_for_table()
            result["table"] = data
        if self.get_is_list():
            data = self.search_for_list()
            result["list"] = data
        FileHandler.save_to_json(result, file_path)

    def save_to_csv(self, file_path):
        if self.get_is_table():
            data, data_fields = self.flat_search("Table")
            table_path = file_path.replace('.csv', '_table.csv')
            FileHandler.save_to_csv(data, data_fields, table_path)
        if self.get_is_list():
            data, data_fields = self.flat_search("List")
            list_path = file_path.replace('.csv', '_list.csv')
            FileHandler.save_to_csv(data, data_fields, list_path)

    def save(self, file_path, data = None):
        if file_path.endswith('.txt'):
            FileHandler.save_to_txt(data, file_path)
        elif file_path.endswith('.csv'):
            self.save_to_csv(file_path)
        elif file_path.endswith('.json'):
            self.save_to_json(file_path)
        else:
            raise ValueError("Invalid file extension. Allowed extensions are: .txt, .csv, .json")