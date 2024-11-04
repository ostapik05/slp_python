from importlib import import_module
from shared.classes.MenuBuilder import MenuBuilder

use_lab = 7

class GlobalUI:
    def __init__(self):
        if use_lab:
            while True:
                self.__run_lab(use_lab)
        self.build_menu()

    def menu(self):
        self.build_menu()
        self._menu.show()

    def build_menu(self):
        self._menu = (
            MenuBuilder()
            .set_title("\nWelcome to specialized programming languages!")
            .set_warning("Wrong input!")
            .set_input_text("Choose lab:")
            .add_option("1", "1. Function calculator\n", self.__run_lab, number=1)
            .add_option("2", "2. OOP calculator\n", self.__run_lab, number=2)
            .add_option("3", "3. ASCII pyfiglet arts\n", self.__run_lab, number=3)
            .add_option("4", "4. ASCII custom arts\n", self.__run_lab, number=4)
            .add_option("5", "5. ASCII 3d\n", self.__run_lab, number=5)
            .add_option("6", "6. Run tests\n", self.__run_lab, number=6)
            .add_option("7", "7. Run API program\n", self.__run_lab, number=7)
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
