from shared.classes.Input import StringInput
from shared.classes.MenuBuilder import MenuBuilder
from shared.classes.ChooseMenuBuilder import ChooseMenuBuilder
from labs.lab7.bll.Controller import Controller
from labs.lab7.ui.DataStyler import DataStyler
import tkinter as tk
from tkinter import filedialog
import pyautogui

class UserInterface:
    def __init__(self, controller: Controller):
        self.controller = controller
        self.styler = DataStyler.default()
        self.regex_menu = self.build_regex_menu()
        self.field_selection_menu = self.build_field_selection_menu()
        self.settings_menu = self.build_settings_menu()
        self.choose_mode_menu = self.build_choose_mode()
        self.choose_fields_menu = self.build_choose_fields_menu()
        self.main_menu = self.build_main()

    def show(self):
        self.main_menu.show()

    def build_main(self):
        menu = (MenuBuilder()
                .set_title("Google Books API\n")
                .set_dynamic_title(self.get_results)
                .add_option("1", "\n1. Input search query", self.set_query)
                .add_option("2", "\n2. Input regular expression", self.regex_menu.show)
                .add_option("3", "\n3. Choose visualization methods", self.choose_visualization_method)
                .add_option("4", "\n4. Settings", self.settings_menu.show)
                .add_option("5", "\n5. Save", self.save)
                .add_stop_options(["0", "Exit", "exit", "e", "q"], "0. Exit")
                .build())
        return menu

    def build_choose_mode(self):
        choose_mode_menu = (ChooseMenuBuilder
                            .unordered()
                            .add_option("1", "List")
                            .add_option("2", "Table")
                            .set_leave_option("0", "Exit")
                            .build())
        return choose_mode_menu

    def build_settings_menu(self):
        settings_menu = (MenuBuilder()
                         .set_title("Settings")
                         .add_option("1", "\n1. List fields", self.choose_fields, mode="List")
                         .add_option("2", "\n2. Table fields", self.choose_fields, mode="Table")
                         .add_stop_options(["0", "Exit", "exit", "e", "q"], "0. Exit")
                         )
        return settings_menu.build()

    def build_choose_fields_menu(self):
        keys = self.controller.get_fields_keys()
        choose_fields_menu = (ChooseMenuBuilder
                              .ordered()
                              .set_leave_option("0", "Exit"))
        for i, field in enumerate(keys):
            choose_fields_menu.add_option(f"{i + 1}", field)
        return choose_fields_menu.build()

    def build_field_selection_menu(self):
        fields_keys = self.controller.get_fields_keys()
        menu = (ChooseMenuBuilder
                .unordered()
                .set_leave_option("0", "Exit")
                .set_is_multiselect(False))
        for index, field in enumerate(fields_keys):
            menu.add_option(f"{index + 1}", field)
        return menu.build()

    def build_regex_menu(self):
        regex_menu = (MenuBuilder()
                      .set_title("Regex string")
                      .set_dynamic_title(self.dynamic_regex_title)
                      .add_option("1", "\n1. Regular expression", self.set_regex)
                      .add_option("2", "\n2. Field", self.set_regex_field)
                      .add_stop_options(["0", "Exit", "exit", "e", "q"], "0. Exit")
                      .build())
        return regex_menu

    def save(self):
        file_path ="C:/Users/oleg0/Desktop/Спеціалізовані МП/labs/src/assets/api data/data.csv"#self.save_file_dialog()
        if file_path == "":
            print("Empty filepath!")
        data = None
        if file_path.endswith('.txt'):
            styled_data = self.get_results()
            data = self.styler.remove_styles(styled_data)
        self.controller.save(file_path, data)
        try:
            t = 13
        except Exception as e:
            print(f"Can't write file. Error {e}")


    def save_file_dialog(self):
        root = tk.Tk()
        root.withdraw()
        default_name = self.controller.get_default_file_name()
        default_path = self.controller.get_default_save_dir()
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"),
                       ("CSV files", "*.csv"),
                       ("JSON files", "*.json"),
                       ("All files", "*.*")],
            initialfile=default_name,
            initialdir=default_path,
            title="Save. You can choose .txt, .csv or .json file types. "
                  "For csv it will create _list.csv or/and _table.csv file if needed"
        )
        root.destroy()
        return file_path or ""

    def dynamic_regex_title(self):
        regex = self.get_regex()
        field = self.get_regex_field()
        return f"{regex} regex string on {field} field"

    def get_regex(self):
        return self.controller.get_regex()

    def get_regex_field(self):
        return self.controller.get_regex_field_name()

    def get_results(self):
        query = self.controller.get_query()
        if not query:
            return "No query yet"
        fields = self.controller.get_fields()
        field_styles = self.controller.get_field_styles()
        is_table = self.controller.get_is_table()
        is_list = self.controller.get_is_list()
        str_results = ""
        if is_table:
            table = self.controller.search_for_table()
            table_data = table[0]
            table_fields = table[1]
            styled_table = self.styler.as_table(table_data, table_fields, field_styles, fields)
            str_results += f"\n{styled_table}"
        if is_list:
            list = self.controller.search_for_list()
            list_data = list[0]
            list_fields = list[1]
            styled_list = self.styler.as_list(list_data, list_fields, field_styles, fields)
            str_results += f"\n{styled_list}"
        regex_string = self.dynamic_regex_title()
        str_results +=f"Query: {query}\n{regex_string}\n"
        return str_results

    def set_query(self):
        min = 3
        max = 30
        query = StringInput().input(f"Enter query {min}-{max}:", [min, max], "Not in range")
        self.controller.set_last_query(query)

    def set_regex(self):
        min = 2
        max = 100
        while True:
            regex = StringInput().input(f"Enter regex {min}-{max}:", [min, max], "Not in range")
            if self.controller.is_regex(regex):
                break
            else:
                print("Wrong regex, try again")
        self.controller.set_last_regex(regex)

    def set_regex_field(self):
        selection_menu = self.field_selection_menu
        selected_field = selection_menu.show()
        self.controller.set_regex_field_name(selected_field)


    def choose_fields(self, attributes):
        mode = attributes.get('mode')
        selected_fields = self.controller.get_selected_fields(mode)
        chosen_fields = (self.choose_fields_menu
                         .set_selected(selected_fields)
                         .show())
        self.controller.set_selected(chosen_fields, mode)

    def choose_visualization_method(self):
        is_list = self.controller.get_is_list()
        is_table = self.controller.get_is_table()
        selected = []
        if is_list:
            selected.append("List")
        if is_table:
            selected.append("Table")
        choose = self.choose_mode_menu.set_selected(selected).show()
        is_list = "List" in choose
        is_table = "Table" in choose
        self.controller.set_is_list(is_list)
        self.controller.set_is_table(is_table)
