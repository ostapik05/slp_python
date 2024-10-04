from abc import ABC, abstractmethod


class AsciiControllerInterface(ABC):
    @abstractmethod
    def get_fonts(self):
        pass

    @abstractmethod
    def set_font(self):
        pass

    @abstractmethod
    def generate_example(self):
        pass
