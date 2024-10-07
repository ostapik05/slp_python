from abc import ABC, abstractmethod


class AsciiGeneratorInterface(ABC):
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
    @abstractmethod
    def replace(data, bright_symbol, empty_symbol):
        pass

    @staticmethod
    @abstractmethod
    def alignment_text(data, alignment, width):
        pass
