from OpenGL.GLUT import *


class MouseHandler:
    def __init__(self, controller):
        self.controller = controller

    def mouse(self, button, state, x, y):
        self.controller.handle_mouse(button, state, x, y)

    def wheel(self, wheel, direction, x, y):
        self.controller.handle_wheel(wheel, direction, x, y)

    def motion(self, x, y):
        self.controller.handle_motion(x, y)
