from shared.classes.MenuBuilder import MenuBuilder
from shared.classes.Input import (
    VariantsInput,
    BoolInput,
    StringInput,
    NumberBetweenInput,
)

from labs.lab3.bll.AsciiController import AsciiController


class AsciiSettingsUI:

    def __init__(self, controller: AsciiController = None):
        self.__controller = controller

    def set_controller(self, controller: AsciiController):
        self.__controller = controller
        self.__menu = self.__menu_build()

    def show(self):
        self.__menu.show()

    def __menu_build(self):
        return (
            MenuBuilder()
            .set_title("Setting for ascii")
            .set_input_text("Choose: ")
            .set_warning("No such setting")
            .set_dynamic_title(self.see_example)
            .add_option_without_attributes(
                "1", "1. Replacing symbols\n", self.set_symbols
            )
            .add_option_without_attributes("2", "2. Change font\n", self.set_font)
            .add_option_without_attributes("3", "3. Change color\n", self.set_color)
            .add_option_without_attributes("4", "4. Change width\n", self.set_width)
            .add_option_without_attributes("5", "5. Change height\n", self.set_height)
            .add_option_without_attributes(
                "6", "6. Change alignment\n", self.set_alignment
            )
            .add_option_without_attributes(
                "7", "7. Change line breaking (word wraping)\n", self.set_line_breaking
            )
            .add_stop_options(["0", "Exit", "exit"], "0. Exit")
            .build()
        )

    def set_symbols(self):
        symbols_menu = (
            MenuBuilder()
            .set_title("Replacing symbols")
            .set_input_text("Choose: ")
            .set_warning("No such setting")
            .set_dynamic_title(self.get_symbols_replacement_info)
            .add_option_without_attributes(
                "1", "1. Set using this symbols\n", self.set_is_replace_symbols
            )
            .add_option_without_attributes(
                "2", "2. Set bright symbols\n", self.set_bright_symbol
            )
            .add_option_without_attributes(
                "3", "3. Set empty symbol\n", self.set_empty_symbol
            )
            .add_stop_options(["0", "Exit", "exit"], "0. Exit")
            .build()
        )
        symbols_menu.show()

    def get_symbols_replacement_info(self):
        bright = self.__controller.get_bright_symbol()
        empty = self.__controller.get_empty_symbol()
        is_replace_symbols = self.__controller.get_is_symbols_replace()
        return (
            f"Current symbols:"
            + f"\n bright: {bright}"
            + f"\n empty: {empty}"
            + f"\n replacing: {is_replace_symbols}"
        )

    def set_alignment(self):
        options = ["left", "right", "center"]
        options_str = "/".join(options)
        message = f"Choose alignment ({options_str}): "
        result = VariantsInput().input(message, options, "Wrong alignment")
        self.__controller.set_alignment(result)

    def set_bright_symbol(self):
        message = "Bright symbol:  "
        result = StringInput.input(message, [1, 1])
        self.__controller.set_bright_symbol(result)

    def set_empty_symbol(self):
        message = "Empty symbol:  "
        result = StringInput.input(message, [1, 1])
        self.__controller.set_empty_symbol(result)

    def set_is_replace_symbols(self):
        message = "Replace (y/n)? "
        result = BoolInput.default(message)
        self.__controller.set_is_symbols_replace(result)

    def set_color(self):
        colors = self.__controller.get_colors()
        colors_str = " ,".join(colors)
        color = VariantsInput().input(
            f"Colors: {colors_str}\n Choose color:", colors, "Wrong color!"
        )
        self.__controller.set_color(color)

    def set_font(self):
        fonts = self.__controller.get_fonts()
        fonts_str = ""
        in_row = 5
        last = 0
        for index in range(0, len(fonts), in_row):
            row = ", ".join(fonts[index : index + in_row])
            fonts_str += "\n" + row

        font = VariantsInput.input(fonts_str + "\nChoose font: ", fonts)
        self.__controller.set_font(font)

    def set_width(self):
        min_width = self.__controller.get_min_width()
        max_width = self.__controller.get_max_possible_width()
        cur_width = self.__controller.get_width()

        message = (
            f"Current width: {cur_width}. Range: {min_width}-{max_width}\n Set width: "
        )
        width = NumberBetweenInput().input(
            message, [min_width, max_width], "Wrong width"
        )
        self.__controller.set_width(width)

    def set_height(self):
        min_height = self.__controller.get_min_height()
        max_height = self.__controller.get_max_possible_height()
        cur_height = self.__controller.get_height()

        message = f"Current height: {cur_height}. Range: {min_height}-{max_height}\n Set height: "
        height = NumberBetweenInput().input(
            message, [min_height, max_height], "Wrong height"
        )
        self.__controller.set_height(height)

    def set_line_breaking(self):
        is_font_support = self.__controller.is_font_support_line_break()
        if is_font_support:
            supporting = "current font support"
        else:
            supporting = "current font not support"
        message = f"Break line/wrap word ({supporting}) (y/n)? "
        result = BoolInput.default(message)
        self.__controller.set_is_line_breaks(result)

    def see_example(self):
        example_text = "Settings for art"
        settings_info = self.__controller.get_settings_info()
        art = self.__controller.create_cutted_art(example_text)
        return settings_info + f"\n '{example_text}' string example\n" + art
