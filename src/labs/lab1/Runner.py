from shared.interfaces.RunnerInterface import RunnerInterface
from config.settings_paths import settings_path_lab1
from labs.lab1.ui import menu


class Runner(RunnerInterface):
    @staticmethod
    def run():
        menu.run(settings_path_lab1)

if __name__ == '__main__':
    Runner.run()