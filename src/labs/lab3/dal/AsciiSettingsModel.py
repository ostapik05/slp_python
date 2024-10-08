from shared.classes.DataAccess import DataAccess

# from shared.interfaces.SettingsInterface import SettingsInterface


class AsciiSettingsModel:

    def __init__(
        self,
        font=None,
        color=None,
        alignment=None,
        height=None,
        width=None,
        bright_symbol=None,
        empty_symbol=None,
        is_symbols_replace=None,
        is_line_breaks=None,
        max_width=500,
        max_height=100,
    ):
        self.font = font
        self.color = color
        self.alignment = alignment
        self.bright_symbol = bright_symbol
        self.empty_symbol = empty_symbol
        self.height = height
        self.width = width
        self.is_symbols_replace = is_symbols_replace
        self.is_line_breaks = is_line_breaks
        self.__max_width = max_width
        self.__max_height = max_height

    @classmethod
    def default(cls):
        instance = cls()
        instance.set_default()
        return instance

    def get_max_width(self):
        return self.__max_width

    def get_max_height(self):
        return self.__max_height

    def set_default(self):
        self.font = "banner"
        self.color = "black"
        self.alignment = "left"
        self.bright_symbol = "@"
        self.empty_symbol = "."
        self.height = 25
        self.width = 80
        self.is_symbols_replace = False
        self.is_line_breaks = True

    def __str__(self):
        return (
            f" Ascii art settings: \n"
            + f"  Font: {self.font} \n"
            + f"  Color: {self.color} \n"
            + f"  Aligment: {self.alignment} \n"
            + f"  Width: {self.width}"
            + f"  Height: {self.height}\n"
            + f"  Bright symbol: {self.bright_symbol}\n"
            + f"  Empty symbol: {self.empty_symbol}\n"
            + f"  Is symbols replace: {self.is_symbols_replace} \n"
        )
