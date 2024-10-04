class Menu:
    def __init__(self):
        self.options = {}
        self.attributes = {}
        self.title = None
        self.dynamic_title = None
        self.text = None
        self.bottom = None
        self.input_text = None
        self.warning = None
        self.is_continue = True

    def set_title(self, title):
        self.title = title

    def set_dynamic_title(self, method):
        self.dynamic_title = method

    def set_input_text(self, input_text):
        self.input_text = input_text

    def set_warning(self, warning):
        self.warning = warning

    def stop(self):
        self.is_continue = False

    def update_option(self, key, message, method, **attributes):
        if not self.text:
            self.text = ""
        if message:
            self.text += message
        self.options[key] = method

        if attributes:
            self.attributes[key] = attributes

    def update_end_option(self, key, message, method, **attributes):
        if not self.bottom:
            self.bottom = ""
        if message:
            self.bottom += message
        self.options[key] = method

        if attributes:
            self.attributes[key] = attributes

    def show_text(self):
        if self.dynamic_title:
            dynamic_title = self.dynamic_title()
            print(dynamic_title)
        if self.title:
            print(self.title)
        if self.text:
            print(self.text)
        if self.bottom:
            print(self.bottom)

    def get_input_and_execute(self):
        user_input = input(self.input_text)
        if user_input not in self.options:
            print(self.warning)
            return
        method = self.options[user_input]
        if user_input in self.attributes:
            method(self.attributes[user_input])
        else:
            method()

    def show(self):
        while True:
            self.show_text()
            self.get_input_and_execute()
            if not self.is_continue:
                break


class MenuBuilder:
    def __init__(self):
        self._menu = Menu()

    def set_title(self, title="Settings"):

        self._menu.set_title(title)
        return self

    def set_dynamic_title(self, method=lambda: "dynamic title"):
        if not callable(method):
            raise ValueError("Wrong dynamic title")
        self._menu.set_dynamic_title(method)
        return self

    def set_input_text(self, input_text="Choose: "):
        self._menu.set_input_text(input_text)
        return self

    def set_warning(self, warning="Wrong option!"):
        self._menu.set_warning(warning)
        return self

    def add_stop_options(self, keys, message="Exit"):
        for key in keys:
            self._menu.update_end_option(key, "", self._menu.stop)
        self._menu.bottom += message
        return self

    def add_option(self, key, message, method, **attributes):
        if not callable(method):
            raise ValueError("Wrong option method")
        self._menu.update_option(key, message, method, **attributes)
        return self

    def add_option_without_attributes(self, key, message, method):
        if not callable(method):
            raise ValueError("Wrong option method")
        self._menu.update_option(key, message, method)
        return self

    def update_attribute(self, key, value):
        self._menu.attributes[key] = value
        return self

    def stop_on_invalid_input(self):
        self._menu.stop()
        return self

    def build(self):
        return self._menu
