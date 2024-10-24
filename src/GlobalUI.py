from logging import Logger
from shared.classes.Input import VariantsInput
from importlib import import_module
from shared.classes.JsonDataAccess import JsonDataAccess
from shared.classes.MenuBuilder import MenuBuilder
from labs.lab4.Runner import Runner


class GlobalUI:
    def __init__(self):

        self.build_menu()

    def menu(self):
        # Runner.run()
        self.build_menu()
        self._menu.show()

    def build_menu(self):
        self._menu = (
            MenuBuilder()
            .set_title("Welcome to specialized programming languages!")
            .set_warning("Wrong input!")
            .set_input_text("Choose lab:")
            .add_option("1", "1. Function calculator\n", self.__run_lab, number=1)
            .add_option("2", "2. OOP calculator\n", self.__run_lab, number=2)
            .add_option("3", "3. ASCII pyfiglet arts\n", self.__run_lab, number=3)
            .add_option("4", "4. ASCII custom arts\n", self.__run_lab, number=4)
            .add_stop_options(["e", "0", "exit", "Exit"], "\n0.Exit(e)")
            .build()
        )

    def __run_lab(self, lab=None):
        if lab is None:
            return
        try:
            numeric = lab["number"]
        except:
            numeric = lab
        module_name = f"labs.lab{numeric}.Runner"
        try:
            runner = import_module(module_name)
        except ImportError:
            print(f"Error: Can't import {module_name}. Please try again.")
            return
        if hasattr(runner.Runner, "run") and callable(runner.Runner.run):
            runner.Runner.run()
        else:
            print(f"Error: 'run' function not found in {module_name}.")
