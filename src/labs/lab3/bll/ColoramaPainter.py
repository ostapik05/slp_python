from shared.interfaces.PaintTextInterface import PaintTextInterface
from colorama import Fore, Style


class ColoramaPainter(PaintTextInterface):

    color_map = {
        "red": Fore.RED,
        "green": Fore.GREEN,
        "yellow": Fore.YELLOW,
        "blue": Fore.BLUE,
        "magenta": Fore.MAGENTA,
        "cyan": Fore.CYAN,
        "white": Fore.WHITE,
        "black": Fore.BLACK,
        "default": Style.RESET_ALL,
    }

    @classmethod
    def paint(cls, text, color):
        if color in cls.color_map:
            return f"{cls.color_map[color]}{text}{Style.RESET_ALL}"
        else:
            raise ValueError(f"Color '{color}' is not supported.")

    @classmethod
    def get_colors(cls):
        return list(cls.color_map.keys())
