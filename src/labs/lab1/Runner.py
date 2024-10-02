from shared.interfaces.RunnerInterface import RunnerInterface
from data.lab1.init import memory, history, available_operations, decimals, log_file
from labs.lab1.ui.menu import menu


class Runner(RunnerInterface):
    @staticmethod
    def run():
        menu(memory, available_operations, decimals, log_file, history)
