from abc import ABC, abstractmethod


class AsciiGenerator(ABC):
    @staticmethod
    @abstractmethod
    def generate(data, **kwargs):
        pass

    @staticmethod
    @abstractmethod
    def is_font_break_lines(font):
        pass

    @staticmethod
    @abstractmethod
    def get_fonts():
        pass

    @staticmethod
    @abstractmethod
    def get_font_char_height(font):
        pass

    @staticmethod
    @abstractmethod
    def get_font_char_width(font):
        pass

    @staticmethod
    def alignment_text(text: str, alignment, width):
        lines = text.splitlines()
        aligned_text = []
        if alignment == "right":
            for row in lines:
                aligned_text.append((" " * (width - len(row) - 1)) + row)
        elif alignment == "center":
            for row in lines:
                free_space_amound = int((width - len(row)) / 2)
                free_space = " " * free_space_amound
                aligned_text.append(free_space + row + free_space)
        elif alignment == "left":
            for row in lines:
                aligned_text.append(row + (" " * (width - len(row) - 1)))
        else:
            raise ValueError("Wrong aligned")
        return "\n".join(aligned_text)

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
