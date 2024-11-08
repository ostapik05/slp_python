from shared.interfaces.RunnerInterface import RunnerInterface
from labs.lab8.init import main

class Runner(RunnerInterface):
    @staticmethod
    def run():
        main()


if __name__ == "__main__":
    Runner.run()