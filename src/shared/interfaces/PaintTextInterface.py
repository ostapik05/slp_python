from abc import ABC, abstractmethod


class PaintTextInterface(ABC):
    @staticmethod
    @abstractmethod
    def paint(text, color):
        pass

    @staticmethod
    @abstractmethod
    def get_colors():
        pass
