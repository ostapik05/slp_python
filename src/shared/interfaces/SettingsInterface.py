from abc import ABC, abstractmethod


class SettingsInterface(ABC):

    @abstractmethod
    def set_default():
        pass

    @abstractmethod
    def save():
        pass

    @abstractmethod
    def load():
        pass

    @abstractmethod
    def __str__():
        pass
