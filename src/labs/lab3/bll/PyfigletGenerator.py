import pyfiglet.fonts
from shared.interfaces.AsciiGeneratorInterface import AsciiGeneratorInterface
from pyfiglet import FigletFont, figlet_format
import re


class PyfigletGenerator(AsciiGeneratorInterface):

    @staticmethod
    def generate(data, **kwargs):

        return figlet_format(data, **kwargs)

    @classmethod
    def is_font_break_lines(cls, font):
        test_line = "testlineforlinebreakingtomuchtofitinsinglelinethatforshure"
        kwargs = {"font": font, "width": 50}
        art = cls.generate(test_line, **kwargs)
        font_height = cls.get_font_char_height(font)
        rows_amound = len(art.splitlines())
        if rows_amound > font_height:
            return True
        else:
            return False

    @staticmethod
    def get_fonts():
        return FigletFont.getFonts()

    @staticmethod
    def replace(data: str, bright_symbol, empty_symbol):
        lines = data.splitlines()
        replaced_lines = []

        for line in lines:
            replaced_line = "".join(
                empty_symbol if char.isspace() else bright_symbol for char in line
            )
            replaced_lines.append(replaced_line)
        replaced_data = "\n".join(replaced_lines)
        return replaced_data

    @classmethod
    def get_font_char_height(cls, font_name):
        try:
            font_data = FigletFont.preloadFont(font_name)
            header_line = font_data.splitlines()[0]
            header_parts = header_line.split()
            header_height = int(header_parts[2])
        except Exception as e:
            print(f"Error retrieving font height: {e}")
            return None
        highest_symbols = "ILQWIONCZ"
        kwargs = {"font": font_name}
        max_height = max(
            len(cls.generate(char, **kwargs).splitlines()) for char in highest_symbols
        )
        return max(header_height, max_height)

    @classmethod
    def get_font_char_width(cls, font_name):
        widest_symbols = "mwGMW"
        kwargs = {"font": font_name}
        max_width = max(
            len(cls.generate(char, **kwargs).splitlines()[0]) for char in widest_symbols
        )
        return max_width

    @staticmethod
    def alignment_text(text: str, alignment, width):
        lines = text.splitlines()
        aligned_text = []
        if alignment == "right":
            for row in lines:
                aligned_text.append((" " * (width - len(row) - 1)) + row)
        elif alignment == "center":
            for row in lines:
                aligned_text.append((" " * int(width - len(row) / 2)) + row)
        elif alignment == "left":
            for row in lines:
                aligned_text.append(row + (" " * (width - len(row) - 1)))
        else:
            raise ValueError("Wrong aligned")
        return "\n".join(aligned_text)
