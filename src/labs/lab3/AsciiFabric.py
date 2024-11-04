
from shared.classes.DictJsonDataAccess import DictJsonDataAccess
from config.settings_paths import settings_path_lab3
from shared.classes.FolderDataAccess import FolderDataAccess
from labs.lab3.bll.AsciiController import AsciiController
from labs.lab3.bll.ColoramaPainter import ColoramaPainter
from labs.lab3.bll.PyfigletGenerator import PyfigletGenerator
from labs.lab3.ui.AsciiSettings import AsciiSettingsUI
from labs.lab3.ui.AsciiMenu import AsciiMenu
from shared.interfaces.UIInterface import UIInterface
from labs.lab4.bll.CustomPainter import CustomPainter
from labs.lab4.bll.CustomGenerator import CustomGenerator


class AsciiFabric:
    def __init__(self, generator=PyfigletGenerator(), coloring=ColoramaPainter()):
        settings_access = DictJsonDataAccess(settings_path_lab3)
        __arts_folder = settings_access.get("__arts_folder")
        settings_ui: UIInterface = AsciiSettingsUI()
        ascii_ui: UIInterface = AsciiMenu(settings_ui, arts_folder= __arts_folder)
        arts_access = FolderDataAccess(__arts_folder, True, ".txt")
        controller = AsciiController(
            generator,
            coloring,
            arts_access,
            settings_access,
        )
        settings_ui.set_controller(controller)
        ascii_ui.set_controller(controller)
        self.__ascii_ui = ascii_ui

    def show(self):
        self.__ascii_ui.show()

    @classmethod
    def pyfiglet(cls):
        generator = PyfigletGenerator()
        coloring = ColoramaPainter()
        return cls(generator, coloring)

    @classmethod
    def custom(cls):
        generator = CustomGenerator()
        coloring = CustomPainter()
        return cls(generator, coloring)
