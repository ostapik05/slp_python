from abc import ABC, abstractmethod


class RunnerInterface(ABC):
    @staticmethod
    def run():
        raise NotImplementedError("Not implemented runner yet")



# if __name__ == '__main__':
#     Runner.run()