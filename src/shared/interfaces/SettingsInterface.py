from abc import ABC, abstractmethod


class SettingsInterface(ABC):

    @abstractmethod
    def set_default(self):
        pass

    @abstractmethod
    def __str__(self):
        pass
