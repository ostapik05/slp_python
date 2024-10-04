from abc import ABC, abstractmethod


class AsciiGeneratorInterface(ABC):
    @staticmethod
    @abstractmethod
    def generate(data, **kwargs):
        pass

    @staticmethod
    @abstractmethod
    def get_fonts():
        pass
