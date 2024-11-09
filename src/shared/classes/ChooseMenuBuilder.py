from shared.classes.Input import *
from shared.classes.OrderedSet import OrderedSet


class ChooseMenu:
    def __init__(self):
        self.options = {}
        self.selected_options = OrderedSet()
        self.leave_option = {'key': 'exit', 'message': 'Exit'}
        self.is_multiselect = True
        self.is_has_order = True
        self.numeric_selected_flag = '[{i}]'
        self.boolean_selected_flag = '[*]'
        self.unselected_flag = '[ ]'
        self.choose_prompt = "Choose from the following options:"
        self.input_prompt = "Enter your choice (number):"
        self.warning_prompt = "Invalid choice. Please try again."
        self.is_continue = True
        self.options_format_string = "{flag}—{key}. {option}"
        self.leave_format_string = "{key}: {message}"

    def set_selected(self, options):
        self.selected_options.clear()
        if isinstance(options, str):
            self.selected_options.add(options)
        else:
            for option in options:
                self.selected_options.add(option)
        return self

    def set_choose_prompt(self, choose_prompt):
        self.choose_prompt = choose_prompt

    def set_input_prompt(self, input_prompt):
        self.input_prompt = input_prompt

    def set_warning_prompt(self, warning_prompt):
        self.warning_prompt = warning_prompt

    def set_is_has_order(self, is_has_order):
        self.is_has_order = is_has_order

    def add_option(self, key, option):
        self.options[key] = option

    def set_leave_option(self, key, leave_option):
        self.leave_option = {"key": key, "message": leave_option}

    def set_is_multiselect(self, is_multiselect):
        self.is_multiselect = is_multiselect

    def set_flags(self, boolean_selected_flag="[*]", numeric_selected_flag="[{i}]", unselected_flag="[ ]"):
        if not self.is_valid_selected_string(boolean_selected_flag):
            raise ValueError("Invalid boolean selected flag")
        self.boolean_selected_flag = boolean_selected_flag
        self.numeric_selected_flag = numeric_selected_flag
        self.unselected_flag = unselected_flag

    def set_options_format_string(self, format_string="{key}: {flag} {option}"):
        if self.is_valid_option_string(format_string):
            self.options_format_string = format_string
        else:
            raise ValueError("Invalid format string")

    def set_leave_format_string(self, format_string="{key}: {message}"):
        if self.is_valid_leave_string(format_string):
            self.leave_format_string = format_string
        else:
            raise ValueError("Invalid format string")

    @staticmethod
    def is_valid_option_string(format_string):
        try:
            format_string.format(key='', flag='', option='')
            return True
        except KeyError:
            return False

    @staticmethod
    def is_valid_selected_string(format_string):
        try:
            format_string.format(i='')
            return True
        except KeyError:
            return False

    @staticmethod
    def is_valid_leave_string(format_string):
        try:
            format_string.format(key='', message='')
            return True
        except KeyError:
            return False

    def get_flag(self, key, value):
        if not self.options[key]:
            raise ValueError("Invalid key")
        if value not in self.selected_options:
            return self.unselected_flag
        if self.is_has_order:
            index = self.selected_options.index(value) + 1
            return self.numeric_selected_flag.format(i=index)
        else:
            return self.boolean_selected_flag

    def display_menu(self):
        print(self.choose_prompt)
        for key, option in self.options.items():
            flag = self.get_flag(key, option)
            print(self.options_format_string.format(key=key, flag=flag, option=option))
        leave_option_key = self.leave_option['key']
        leave_option_message = self.leave_option['message']
        print(self.leave_format_string.format(key=leave_option_key, message=leave_option_message))

    def get_input_and_execute(self):
        while self.is_continue:
            self.display_menu()
            leave_option_key = self.leave_option['key']
            option_keys = list(self.options.keys()) + [leave_option_key]
            selected_key = VariantsInput().input(self.input_prompt, option_keys, self.warning_prompt,
                                                 not self.is_continue)
            if selected_key in (leave_option_key, None):
                self.stop()
                break
            selected_value = self.options[selected_key]
            if selected_value in self.selected_options:
                self.selected_options.remove(selected_value)
                continue
            if not self.is_multiselect:
                self.selected_options.clear()
            self.selected_options.add(selected_value)

    def stop(self):
        self.is_continue = False

    def show(self):
        self.is_continue = True
        self.get_input_and_execute()
        options = self.selected_options
        return options



class ChooseMenuBuilder:
    def __init__(self):
        self.menu = ChooseMenu()

    @classmethod
    def ordered(cls):
        return (cls()
                .set_choose_prompt("Select:")
                .set_is_multiselect(True)
                .set_is_has_order(True)
                .set_flags(numeric_selected_flag='[{i}]', unselected_flag='[ ]')
                .set_input_prompt("Enter number:")
                .set_options_format_string("{key}: {flag} {option}")
                .set_warning_prompt("not in variants, please select a valid number.")
                .set_leave_option("0", "Finish selection")
                .set_leave_format_string("{key}: {message}")
                )

    @classmethod
    def unordered(cls):
        return (cls()
                .set_choose_prompt("Select:")
                .set_is_multiselect(True)
                .set_is_has_order(False)
                .set_flags(boolean_selected_flag='[*]', unselected_flag='[ ]')
                .set_input_prompt("Choose:")
                .set_options_format_string("{key}: {flag} {option}")
                .set_warning_prompt(" — wrong input.")
                .set_leave_option("Exit", "Finish selection")
                .set_leave_format_string("{key}: {message}")
                )

    def set_selected(self, options):
        self.menu.set_selected(options)

    def set_choose_prompt(self, choose_prompt):
        self.menu.set_choose_prompt(choose_prompt)
        return self

    def set_input_prompt(self, input_prompt):
        self.menu.set_input_prompt(input_prompt)
        return self

    def set_warning_prompt(self, warning_prompt):
        self.menu.set_warning_prompt(warning_prompt)
        return self

    def set_is_has_order(self, is_has_order):
        self.menu.set_is_has_order(is_has_order)
        return self

    def add_option(self, key, option):
        self.menu.add_option(key, option)
        return self

    def set_leave_option(self, key, leave_option):
        self.menu.set_leave_option(key, leave_option)
        return self

    def set_is_multiselect(self, is_multiselect):
        self.menu.set_is_multiselect(is_multiselect)
        return self

    def set_flags(self, boolean_selected_flag="[*]", numeric_selected_flag="[{i}]", unselected_flag="[ ]"):
        self.menu.set_flags(boolean_selected_flag, numeric_selected_flag, unselected_flag)
        return self

    def set_options_format_string(self, format_string="{key}: {flag} {option}"):
        self.menu.set_options_format_string(format_string)
        return self

    def set_leave_format_string(self, format_string="{key}: {message}"):
        self.menu.set_leave_format_string(format_string)
        return self

    def build(self):
        for selected in self.menu.selected_options:
            if selected not in self.menu.options:
                raise ValueError(f"Select {selected}, but not in variants({self.menu.options})")
        return self.menu

