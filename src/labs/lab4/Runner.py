from shared.interfaces.RunnerInterface import RunnerInterface
from labs.lab3.AsciiFabric import AsciiFabric


class Runner(RunnerInterface):
    @staticmethod
    def run():
        AsciiFabric.custom().show()
