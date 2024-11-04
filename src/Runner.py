from GlobalUI import GlobalUI
from shared.interfaces.RunnerInterface import RunnerInterface


class Runner(RunnerInterface):
    @staticmethod
    def run():
        GlobalUI().menu()

if __name__ == "__main__":
    Runner.run()
