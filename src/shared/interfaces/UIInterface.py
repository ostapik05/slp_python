from abc import ABC, abstractmethod


class UIInterface(ABC):
    @abstractmethod
    def show():
        pass

    @abstractmethod
    def set_controller():
        pass
