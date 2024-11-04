from abc import ABC, abstractmethod


class UIInterface(ABC):
    @abstractmethod
    def show(self):
        pass

    @abstractmethod
    def set_controller(self):
        pass
