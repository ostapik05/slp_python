from labs.lab5.bll.Scene import Scene
from labs.lab5.bll.CameraWrapper import Camera
from labs.lab5.bll.FigureWrapper import FigureWrapper
from labs.lab5.bll.Controller import Controller
from labs.lab5.dal.Camera import CameraData
from labs.lab5.config import *
from labs.lab5.ui.Keyboard import KeyboardHandler
from labs.lab5.ui.Mouse import MouseHandler
from shared.classes.MenuBuilder import MenuBuilder
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


def create_scene():
    scene = Scene()
    camera = Camera(CameraData([0, 0, 5], [0, 0, 0], [0, 1, 0]))
    scene.set_camera(camera)
    cube = FigureWrapper.create('Cube')
    cube.translate(4, -2, 1)
    cube.set_color("Green")
    pyramid = FigureWrapper.create('Pyramid')
    pyramid.rotate(45, 0, 0)
    pyramid.scale(1.1, 1.5, 0.4)
    pyramid.set_color("Red")
    sphere = FigureWrapper.create('Sphere')
    sphere.translate(-1, 3, 5)
    sphere.set_color('Blue')
    scene.add_figure(cube)
    scene.add_figure(pyramid)
    scene.add_figure(sphere)
    return scene

def set_up(scene):
    controller = Controller(scene)
    keyboard_handler = KeyboardHandler(controller)
    mouse_handler = MouseHandler(controller)
    return controller, keyboard_handler, mouse_handler

def init_glut(controller, keyboard_handler, mouse_handler):
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH | GLUT_STENCIL)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutCreateWindow(GLUT_WINDOW_TITLE)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(PERSPECTIVE_ANGLE, WINDOW_WIDTH / WINDOW_HEIGHT, NEAR_CLIP, FAR_CLIP)
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_STENCIL_TEST)
    glDisable(GL_LIGHTING)
    glutDisplayFunc(controller.display)
    glutReshapeFunc(controller.reshape)
    glutSpecialFunc(keyboard_handler.special_keyboard)
    glutSpecialUpFunc(keyboard_handler.special_keyboard_up)
    glutKeyboardFunc(keyboard_handler.keyboard)
    glutKeyboardUpFunc(keyboard_handler.keyboard_up)
    glutMouseFunc(mouse_handler.mouse)
    glutMotionFunc(mouse_handler.motion)
    glutMouseWheelFunc(mouse_handler.wheel)
    glutMainLoop()

# def menu_init():
#     menu = MenuBuilder().set_title(TITLE)


def main():
    scene = create_scene()
    controller, keyboard_handler, mouse_handler = set_up(scene)
    init_glut(controller, keyboard_handler, mouse_handler)
