from shared.classes.OrderedSet import OrderedSet
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from labs.lab5.dal.Keyboard import action_keys, shortcuts, glut_keys_modifiers
from labs.lab5.ui.Screen import *
from config.settings_paths import settings_path_lab5
from shared.classes.DictJsonDataAccess import DictJsonDataAccess

class Controller:
    def __init__(self, scene, buffer = None):
        self.scene = scene
        self.buffer = buffer
        self.pressed_keys = OrderedSet()
        self.settings = DictJsonDataAccess(settings_path_lab5)
        self.action_values = {
            'draw_points': {
                'action': self.set_draw_mode,
                'args': ('points',)
            },
            'draw_edges': {
                'action': self.set_draw_mode,
                'args': ('edges',)
            },
            'draw_faces': {
                'action': self.set_draw_mode,
                'args': ('faces',)
            },
            'translate_left': {
                'action': self.translate_figure_or_camera,
                'args': (-0.5, 0, 0)
            },
            'translate_right': {
                'action': self.translate_figure_or_camera,
                'args': (0.5, 0, 0)
            },
            'translate_forward': {
                'action': self.translate_figure_or_camera,
                'args': (0, 0, -0.5)
            },
            'translate_backward': {
                'action': self.translate_figure_or_camera,
                'args': (0, 0, 0.5)
            },
            'translate_up': {
                'action': self.translate_figure_or_camera,
                'args': (0, 0.5, 0)
            },
            'translate_down': {
                'action': self.translate_figure_or_camera,
                'args': (0, -0.5, 0)
            },
            'rotate_x_plus': {
                'action': self.rotate_figure_or_camera,
                'args': (0, -5, 0)
            },
            'rotate_x_minus': {
                'action': self.rotate_figure_or_camera,
                'args': (0, 5, 0)
            },
            'rotate_y_plus': {
                'action': self.rotate_figure_or_camera,
                'args': (5, 0, 0)
            },
            'rotate_y_minus': {
                'action': self.rotate_figure_or_camera,
                'args': (-5, 0, 0)
            },
            'increase_render_distance': {
                'action': self.change_camera_perspective,
                'args': (None, None, None, +10.)
            },
            'decrease_render_distance': {
                'action': self.change_camera_perspective,
                'args': (None, None, None, -10.)
            },
            'zoom_up': {
                'action': self.change_camera_perspective,
                'args': (-5., None, None, None)
            },
            'zoom_down': {
                'action': self.change_camera_perspective,
                'args': (5., None, None, None)
            },
            'exit': {
                'action': self.exit,
                'args': ()
            }
        }
    def handle_actions(self, modifiers):
        for pressed_key in self.pressed_keys:
            if modifiers:
                action_name = shortcuts.get(modifiers).get(pressed_key)
                if not action_name:
                    continue
                self.execute_command(action_name)
                break
            if pressed_key not in action_keys.keys():
                continue
            action_name = action_keys.get(pressed_key)
            self.execute_command(action_name)

    def handle_keyboard_up(self, key):
        if isinstance(key, bytes):
            try:
                key = key.decode('utf-8')
            except UnicodeDecodeError:
                # TODO add other languages support
                return
        if key in glut_keys_modifiers.keys():
            key = glut_keys_modifiers.get(key)
        self.pressed_keys.discard(key)


    def handle_keyboard(self, key, modifiers):

        if isinstance(key, bytes):
            try:
                key = key.decode('utf-8')
            except UnicodeDecodeError:
                # TODO add other languages support
                return
        key.lower()
        if key in glut_keys_modifiers.keys():
            key = glut_keys_modifiers.get(key)
        self.pressed_keys.add(key)
        self.handle_actions(modifiers)
        glutPostRedisplay()

    def handle_mouse(self, button, state, x, y):
        if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
            self.scene.handle_click(x, y, button)
        elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
            self.scene.data.is_rotating = True
            self.scene.data.last_mouse_x = x
            self.scene.data.last_mouse_y = y
        elif button == GLUT_RIGHT_BUTTON and state == GLUT_UP:
            self.scene.data.is_rotating = False
        glutPostRedisplay()

    def handle_wheel(self, wheel, direction, x, y):
        if direction > 0:
            self.execute_command('zoom_up')
        else:
            self.execute_command('zoom_down')
        glutPostRedisplay()

    def handle_motion(self, x, y):
        self.scene.handle_motion(x, y)


    def execute_command(self, action_key):
        command = self.action_values.get(action_key)
        if not command:
            return
        action = command.get('action')
        args = command.get('args')
        action(*args)
        glutPostRedisplay()

    def reset_perspective(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        fov = self.scene.data.camera.data.fovy if self.scene.data.camera.data else 45.0
        aspect = glutGet(GLUT_WINDOW_WIDTH) / max(glutGet(GLUT_WINDOW_HEIGHT), 1)
        z_near = self.scene.data.camera.data.z_near if self.scene.data.camera.data else 1.0
        z_far = self.scene.data.camera.data.z_far if self.scene.data.camera.data else 50.0
        gluPerspective(fov, aspect, z_near, z_far)
        glMatrixMode(GL_MODELVIEW)
        glutPostRedisplay()


    def display(self):
        if self.buffer:
            self.buffer.display(self.scene.draw)
            return
        scene_draw_func = self.scene.draw
        display(scene_draw_func)


    def reshape(self, width, height):
        fov = self.scene.data.camera.data.fovy if self.scene.data.camera.data else 45.
        aspect = width / height if width and height else 1.5
        z_near = self.scene.data.camera.data.z_near if self.scene.data.camera.data else 1.
        z_far = self.scene.data.camera.data.z_far if self.scene.data.camera.data else 50.
        reshape(width, height, fov, aspect, z_near, z_far)


    def set_draw_mode(self, draw_mode):
        if self.scene.data.selected_figure:
            self.scene.data.selected_figure.set_draw_mode(draw_mode)
        else:
            for figure in self.scene.data.figures:
                figure.set_draw_mode(draw_mode)


    def translate_figure_or_camera(self, x, y, z):
        if self.scene.data.selected_figure:
            self.scene.data.selected_figure.translate(x, y, z)
        else:
            self.scene.data.camera.translate(x, y, z)


    def rotate_figure_or_camera(self, dx, dy, dz):
        if self.scene.data.selected_figure:
            self.scene.data.selected_figure.rotate(dx, dy, dz)
        else:
            self.scene.data.camera.rotate(dx, dy, dz)


    def change_camera_perspective(self, delta_fovy, aspect, delta_z_near, delta_z_far):
        if delta_z_far is not None:
            self.scene.data.camera.update_z_far(delta_z_far)
        if delta_fovy is not None:
            self.scene.data.camera.update_fovy(delta_fovy)
        if aspect is not None:
            self.scene.data.camera.update_aspect(aspect)
        if delta_z_near is not None:
            self.scene.data.camera.update_z_near(delta_z_near)
        self.reset_perspective()

    def exit(self):
        glutLeaveMainLoop()