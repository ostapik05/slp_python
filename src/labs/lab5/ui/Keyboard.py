from labs.lab5.dal.Keyboard import glut_keys_modifiers
from OpenGL.GLUT import *

class KeyboardHandler:
    def __init__(self, controller):
        self.controller = controller

    def special_keyboard_up(self, key, x, y):
        str_key = glut_keys_modifiers.get(key)
        if str_key:
            self.keyboard_up(str_key, x, y)

    def special_keyboard(self, key, x, y):
        str_key = glut_keys_modifiers.get(key)
        if str_key:
            self.keyboard(str_key, x, y)

    def keyboard_up(self, key, x, y):
        if isinstance(key, bytes):
            try:
                key = key.decode('utf-8')
            except UnicodeDecodeError:
                # TODO add other languages support
                return
        self.controller.handle_keyboard_up(key)


    def keyboard(self, key, x, y):
        modifiers = glutGetModifiers()
        self.controller.handle_keyboard(key, modifiers)


