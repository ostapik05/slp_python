from labs.lab5.dal.Keyboard import keys_map
from OpenGL.GLUT import *

class KeyboardHandler:
    def __init__(self, controller = None):
        self.controller = controller

    def set_controller(self, controller):
        self.controller = controller

    def special_keyboard_up(self, key, x, y):
        str_key = keys_map.get(key)
        if str_key:
            self.keyboard_up(str_key, x, y)

    def special_keyboard(self, key, x, y):
        str_key = keys_map.get(key)
        if str_key:
            self.keyboard(str_key, x, y)

    def keyboard_up(self, key, x, y):
        if isinstance(key, bytes):
            try:
                key = key.decode('utf-8')
            except UnicodeDecodeError:
                #can add more languages here
                return
        self.controller.handle_keyboard_up(key)


    def keyboard(self, key, x, y):
        modifiers = glutGetModifiers()
        if isinstance(key, bytes):
            try:
                key = key.decode('utf-8')
            except UnicodeDecodeError:
                #can add more languages here
                return
        key.lower()
        new_key = keys_map.get(key)
        if new_key:
            key = new_key
        if modifiers:
            modifiers = keys_map.get(key)
        self.controller.handle_keyboard(key, modifiers)


