from shared.interfaces.UIInterface import UIInterface
from config.GlobalVariables import lab_amound
from shared.classes.VariantsInput import VariantsInput
from importlib import import_module
from shared.interfaces.RunnerInterface import RunnerInterface

from labs.lab1.Runner import Runner


class GlobalUI(UIInterface):
    @staticmethod
    def menu():
        while True:
            variants = [str(num) for num in range(1, lab_amound + 1)]
            variants.append("q")

            variant = VariantsInput.input(
                f"Write lab number 1-{lab_amound} or 'q' to quit: ", variants
            )

            if variant == "q":
                print("End of program")
                return

            module_name = f"labs.lab{variant}.Runner"
            try:
                runner = import_module(module_name)
            except ImportError:
                print(f"Error: Can't import {module_name}. Please try again.")
                continue

            if hasattr(runner.Runner, "run") and callable(runner.Runner.run):
                runner.Runner.run()
            else:
                print(f"Error: 'run' function not found in {module_name}.")
