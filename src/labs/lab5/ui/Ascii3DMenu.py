from shared.classes.MenuBuilder import MenuBuilder
from shared.interfaces.UIInterface import UIInterface
from shared.classes.Input import StringInput, NumberBetweenInput, BoolInput
from labs.lab5.bll.Controller import Controller


class Ascii3DMenu(UIInterface):
    def __init__(self, controller: Controller = None):
        self.controller = controller
        if controller:
            self.set_controller(controller)

    def set_controller(self, controller: Controller):
        self.controller = controller
        self.menu = self.__menu_build()

    def show(self):
        self.menu.show()

    def __menu_build(self):
        return (
            MenuBuilder()
            .set_title("\nAscii 3D scene generator\n")
            .set_warning("Wrong input!")
            .set_input_text("Choose: ")
            .add_option("1", "1. Make scene\n", self.make_scene)
            .add_option("2", "2. Specify file to save\n", self.save_scene)
            .add_option("3", "3. Set height\n", self.set_height)
            .add_stop_options(["0", "Exit", "exit"], "0. Exit")
            .build()
        )

    def make_scene(self):
        if not self.controller.file_name:
            message = "File to save not specified, you want to save(y, n)?"
            warning_message = "Wrong input, choose y or n"
            result = BoolInput().input(message, ["y", "n"], warning_message)
            if result:
                return
        else:
            print(f"Will save your scene in {self.controller.file_name}")
        self.controller.make_scene()



    def save_scene(self):
        message = "Write name: "
        limit = 30  # hardcode variable of key length
        file_name = StringInput().input(message, [1, limit], "Too long") + ".txt"
        self.controller.set_file_name(file_name)


    def set_height(self):
        min_height = 3
        max_height = 20
        message = f"Set height { min_height }-{ max_height}: "
        warning_message = "Wrong height"
        input = NumberBetweenInput().input(message, [min_height, max_height], warning_message)
        try:
            input = int(input)
        except:
            return
        self.controller.set_height(input)


