class Menu:
    def __init__(self):
        self.options = {}
        self.attributes = {}
        self.title = "Title"
        self.dynamic_title = None
        self.text = None
        self.bottom = None
        self.input_text = "Choose:"
        self.warning = "Wrong option!"
        self.is_continue = True
        self.end_callback = None
        self.end_callback_attributes = None

    def set_title(self, title):
        self.title = title

    def set_dynamic_title(self, method):
        self.dynamic_title = method

    def get_print_text(self):
        parts = filter(None, [
            self.title,
            self.dynamic_title() if self.dynamic_title else None,
            self.text,
            self.bottom,
        ])
        return "\n".join(parts)

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

    def update_end_callback(self,method, **attributes):
        if not callable(method):
            raise ValueError("Wrong end callback")
        self.end_callback = method
        if attributes:
            self.end_callback_attributes = attributes

    def show_text(self):
        text = self.get_print_text()
        print(text)


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
        self.is_continue = True
        while True:
            self.show_text()
            self.get_input_and_execute()
            if not self.is_continue:
                break
        if self.end_callback:
            self.end_callback(self.attributes) if self.end_callback_attributes else self.end_callback()


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

    def update_end_callback(self,end_callback, **attributes):
        self._menu.update_end_callback(end_callback, **attributes)
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
