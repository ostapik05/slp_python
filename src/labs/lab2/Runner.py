from config.settings_paths import settings_path_lab2
from labs.lab2.ui.Calculator import Calculator
from shared.interfaces.RunnerInterface import RunnerInterface


class Runner(RunnerInterface):
    @staticmethod
    def run():
        calculator = Calculator(
            settings_path_lab2
        )
        calculator.menu()


if __name__ == "__main__":
    Runner.run()
