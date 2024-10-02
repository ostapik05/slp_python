from abc import ABC, abstractmethod


class RunnerInterface(ABC):

    @abstractmethod
    def run():
        pass
