from shared.interfaces.PaintTextInterface import PaintTextInterface


class CustomPainter(PaintTextInterface):

    color_map = {
        "red": "\x1b[31m",
        "green": "\x1b[32m",
        "yellow": "\x1b[33m",
        "blue": "\x1b[34m",
        "magenta": "\x1b[35m",
        "cyan": "\x1b[36m",
        "white": "\x1b[97m",
        "light_gray": "\x1b[37m",
        "dark_gray": "\x1b[90m",
        "black": "\x1b[30m",
        "default": "\x1b[0m",
    }

    @classmethod
    def paint(cls, text, color):
        if color in cls.color_map:
            start_color = cls.color_map[color]
            end_color = cls.color_map["default"]
            return f"{start_color}{text}{end_color}"
        else:
            raise ValueError(f"Color '{color}' is not supported.")

    @classmethod
    def get_colors(cls):
        return list(cls.color_map.keys())
