from shared.interfaces.AsciiGeneratorInterface import AsciiGeneratorInterface
from shared.interfaces.PaintTextInterface import PaintTextInterface
from shared.classes.KeyDataAccess import KeyDataAccess
from shared.classes.DataAccess import DataAccess
from labs.lab3.dal.AsciiSettingsModel import AsciiSettingsModel


class AsciiController:

    def __init__(
        self,
        generator: AsciiGeneratorInterface,
        coloring: PaintTextInterface,
        arts_access: KeyDataAccess,
        settings_access: DataAccess[AsciiSettingsModel],
    ):
        self._generator = generator
        self._coloring = coloring
        self._arts_access = arts_access
        # model = AsciiSettingsModel.default()
        # settings_access.set(model)
        self._settings_access = settings_access
        self.art = None

    def _get_model(self) -> AsciiSettingsModel:
        return self._settings_access.get()

    def _set_model(self, model: AsciiSettingsModel):
        return self._settings_access.set(model)

    def get_fonts(self):
        return self._generator.get_fonts()

    def get_font(self):
        model = self._get_model()
        return model.font

    def set_font(self, font):
        if not font in self.get_fonts():
            raise ValueError("Font not in fonts list")
        model = self._get_model()
        model.font = font
        self._set_model(model)

    def get_bright_symbol(self):
        model = self._get_model()
        return model.bright_symbol

    def get_empty_symbol(self):
        model = self._get_model()
        return model.empty_symbol

    def set_bright_symbol(self, symbol):
        if len(symbol) != 1:
            raise ValueError("String with wrong lenghts, can't set symbol")
        model = self._get_model()
        model.bright_symbol = symbol
        self._set_model(model)

    def set_empty_symbol(self, symbol):
        if len(symbol) != 1:
            raise ValueError("String with wrong lenghts, can't set symbol")
        model = self._get_model()
        model.empty_symbol = symbol
        self._set_model(model)

    def set_is_symbols_replace(self, is_symbols_replace):
        if is_symbols_replace not in [True, False]:
            raise ValueError("Try set non-bool value to using symbols")
        model = self._get_model()
        model.is_symbols_replace = is_symbols_replace
        self._set_model(model)

    def get_is_symbols_replace(self):
        model = self._get_model()
        return model.is_symbols_replace

    def get_colors(self):
        return self._coloring.get_colors()

    def set_color(self, color):
        if not color in self.get_colors():
            raise ValueError("Color not in colors list")
        model = self._get_model()
        model.color = color
        self._set_model(model)

    def get_min_width(self):
        model = self._get_model()
        font = model.font
        return self._generator.get_font_char_width(font)

    def get_min_height(self):
        model = self._get_model()
        font = model.font
        return self._generator.get_font_char_height(font)

    def is_font_support_line_break(self):
        font = self.get_font()
        return self._generator.is_font_break_lines(font)

    def get_char_limit(self):
        font_height = self.get_min_height()
        font_width = self.get_min_width()
        height_limit = self.get_height()
        width_limit = self.get_width()
        if font_height > height_limit:
            return 0
        if font_width > width_limit:
            return 0
        symbols_in_row = int(width_limit / font_width)
        is_line_breaks = self.get_is_line_breaks()
        is_font_breaks_line = self.is_font_support_line_break()
        if not is_line_breaks or not is_font_breaks_line:
            return symbols_in_row
        cols = int(height_limit / font_height)
        return symbols_in_row * cols

    def get_max_possible_width(self):
        model = self._get_model()
        return model.get_max_width()

    def get_max_possible_height(self):
        model = self._get_model()
        return model.get_max_height()

    def get_width(self):
        model = self._get_model()
        return model.width

    def get_height(self):
        model = self._get_model()
        return model.height

    def set_height(self, height):
        try:
            height = int(height)
        except:
            raise TypeError("Wrong type of width")

        model = self._get_model()
        max_height = model.get_max_height()
        min_height = self.get_min_height()
        if not min_height <= height <= max_height:
            raise ValueError("Height not in diapason")
        model.height = height
        self._set_model(model)

    def set_width(self, width):
        try:
            width = int(width)
        except:
            raise TypeError("Wrong type of width")
        model = self._get_model()
        max_width = model.get_max_width()
        min_width = self.get_min_width()
        if not min_width <= width <= max_width:
            raise ValueError("Width not in diapason")
        model.width = width
        self._settings_access.set(model)

    def get_alignment(self):
        model = self._get_model()
        alignment = model.alignment
        return alignment

    def set_alignment(self, alignment):
        options = ["left", "right", "center"]
        if alignment not in options:
            raise ValueError("Wrong alignment")
        model = self._get_model()
        model.alignment = alignment
        self._settings_access.set(model)

    def get_is_line_breaks(self):
        return self._get_model().is_line_breaks

    def set_is_line_breaks(self, is_line_breaks):
        if is_line_breaks not in [True, False]:
            raise ValueError("Try set non-bool value to line breaking")
        model = self._get_model()
        model.is_line_breaks = is_line_breaks
        self._set_model(model)

    def is_line_broken(self, art: str):
        is_symbol_replace = self.get_is_symbols_replace()
        bright_symbol = self.get_bright_symbol() if is_symbol_replace else None
        is_symbol_detected = False
        is_gap_detected = False

        for line in art.splitlines():
            line_has_content = (
                bright_symbol in line if is_symbol_replace else line.strip()
            )

            if line_has_content:
                is_symbol_detected = True
                if is_gap_detected:
                    return True
            else:
                if is_symbol_detected:
                    is_gap_detected = True

        return False

    def is_art_exist(self):
        return bool(self.art)

    def get_art(self):
        return self.art

    def set_art(self, art):
        if not art:
            raise ValueError("No art to set")
        self.art = art

    def save_art(self, name):
        art = self.get_art()
        if not art:
            raise ValueError("No art to save")
        if not self.is_art_allowed(art):
            raise ValueError("Too wide")
        self._arts_access.set(name, art)

    def remove_color(string):
        result = []
        in_ansi_sequence = False
        for char in string:
            if char == "\x1b":
                in_ansi_sequence = True
            elif in_ansi_sequence and char == "m":
                in_ansi_sequence = False
            elif not in_ansi_sequence:
                result.append(char)
        return "".join(result)

    def is_art_allowed(self, art: str):
        lines = art.splitlines()
        if not lines:
            return False
        art_height = len(lines)
        art_weight = len(lines[1])
        height_limit = self.get_height()
        width_limit = self.get_width()
        if art_height > height_limit:
            return False

        if art_weight > width_limit:
            return False
        is_line_breaks = self.get_is_line_breaks()
        if not is_line_breaks:
            is_line_broken = self.is_line_broken(art)
            if is_line_broken:
                return False
        return True

    def generate(self, text, width=None):
        font = self._get_model().font
        if width == None:
            width = self.get_width()
        kwargs = {"font": font, "width": width}

        art = self._generator.generate(text, **kwargs)
        return art

    def replace(self, art):
        bright = self.get_bright_symbol()
        empty = self.get_empty_symbol()
        return self._generator.replace(art, bright, empty)

    def paint(self, art):
        color = self._get_model().color
        return self._coloring.paint(art, color)

    def cut(self, text, width, height):
        lines = text.split("\n")
        lines = lines[0 : height - 1]
        cutted_lines = []
        for line in lines:
            cutted_lines.append(line[0 : width - 1])
        return "\n".join(cutted_lines)

    def justify(self, text):
        alignment = self.get_alignment()
        width = self.get_width()
        justified_text = self._generator.alignment_text(text, alignment, width)
        return justified_text

    def create_art(self, text):
        art = self.generate(text)
        is_allowed = self.is_art_allowed(art)
        if not is_allowed:
            raise ValueError("Art breaks the rules")
        justified_art = self.justify(art)
        is_replace = self.get_is_symbols_replace()
        if is_replace:
            justified_art = self.replace(justified_art)
        self.set_art(justified_art)
        painted_art = self.paint(justified_art)
        return painted_art

    def create_cutted_art(self, text):
        is_line_breaks = self.get_is_line_breaks()
        if not is_line_breaks:
            art = self.generate(text, 999)
        else:
            art = self.generate(text)
        width = self.get_width()
        height = self.get_height()
        cutted_art = self.cut(art, width, height)
        justified_art = self.justify(cutted_art)
        is_replace = self.get_is_symbols_replace()
        if is_replace:
            justified_art = self.replace(justified_art)

        painted_art = self.paint(justified_art)
        return painted_art

    def get_settings_info(self):
        model = self._get_model()
        return model.__str__()
