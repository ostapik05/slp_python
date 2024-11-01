import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

from collections import OrderedDict

GLUT_WINDOW_TITLE = b"3D Scene with PyOpenGL"  # Use a regular string for the title
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 250
PERSPECTIVE_ANGLE = 45
NEAR_CLIP = 1.0
FAR_CLIP = 50.0


class OrderedSet:
    def __init__(self):
        self._data = OrderedDict()

    def add(self, item):
        if item not in self._data:
            self._data[item] = None

    def discard(self, item):
        if item in self._data:
            del self._data[item]

    def remove(self, item):
        if item in self._data:
            del self._data[item]
        else:
            raise KeyError(f"Item {item} not found in OrderedSet")

    def __contains__(self, item):
        return item in self._data

    def __repr__(self):
        return f"{', '.join(self._data.keys())}"

    def __iter__(self):
        return iter(self._data.keys())


class Figure3D:
    def __init__(self, vertices, edges, faces=None, color=(1, 1, 1), draw_mode='edges'):
        self.vertices = np.array(vertices, dtype=np.float32)
        self.edges = edges
        self.faces = faces if faces is not None else []
        self.color = color
        self.angle = [0, 0, 0]
        self.draw_mode = draw_mode
        self.selected = False

    def rotate(self, dx, dy, dz):
        center = np.mean(self.vertices, axis=0)
        self.translate(-center[0], -center[1], -center[2])

        angle_rad_x = math.radians(dx)
        angle_rad_y = math.radians(dy)
        angle_rad_z = math.radians(dz)

        rotation_matrix_x = np.array([
            [1, 0, 0],
            [0, math.cos(angle_rad_x), -math.sin(angle_rad_x)],
            [0, math.sin(angle_rad_x), math.cos(angle_rad_x)]
        ])

        rotation_matrix_y = np.array([
            [math.cos(angle_rad_y), 0, math.sin(angle_rad_y)],
            [0, 1, 0],
            [-math.sin(angle_rad_y), 0, math.cos(angle_rad_y)]
        ])

        rotation_matrix_z = np.array([
            [math.cos(angle_rad_z), -math.sin(angle_rad_z), 0],
            [math.sin(angle_rad_z), math.cos(angle_rad_z), 0],
            [0, 0, 1]
        ])

        rotation_matrix = np.dot(np.dot(rotation_matrix_z, rotation_matrix_y), rotation_matrix_x)

        self.vertices = np.dot(self.vertices, rotation_matrix.T)
        self.translate(center[0], center[1], center[2])
        self.angle = [angle + delta for angle, delta in zip(self.angle, [dx, dy, dz])]

    def translate(self, x, y, z):
        translation_matrix = np.array([x, y, z], dtype=np.float32)
        self.vertices += translation_matrix

    def set_draw_mode(self, mode):
        if mode in ['points', 'edges', 'faces']:
            self.draw_mode = mode

    def draw_points(self):
        glColor3fv(self.color)
        glPointSize(5 if self.selected else 1)
        glBegin(GL_POINTS)
        for vertex in self.vertices:
            glVertex3fv(vertex)
        glEnd()

    def draw_edges(self):
        glColor3fv(self.color)
        glLineWidth(2 if self.selected else 1)
        glBegin(GL_LINES)
        for edge in self.edges:
            for vertex in edge:
                glVertex3fv(self.vertices[vertex])
        glEnd()

    def draw_faces(self):
        face_color = (*self.color, 0.5)
        glColor4fv(face_color)
        glBegin(GL_QUADS)
        for face in self.faces:
            for vertex in face:
                glVertex3fv(self.vertices[vertex])
        glEnd()

        if self.selected:
            border_color = (1, 1, 1) if sum(self.color) <= 1.5 else (0, 0, 0)
            glColor3fv(border_color)
            glLineWidth(2)
            glBegin(GL_LINES)
            for face in self.faces:
                for i in range(len(face)):
                    start_vertex = self.vertices[face[i]]
                    end_vertex = self.vertices[face[(i + 1) % len(face)]]
                    glVertex3fv(start_vertex)
                    glVertex3fv(end_vertex)
            glEnd()

    def draw(self):
        glPushMatrix()
        if self.draw_mode == 'points':
            self.draw_points()
        elif self.draw_mode == 'edges':
            self.draw_edges()
        elif self.draw_mode == 'faces':
            self.draw_faces()
        glPopMatrix()

    def project_vertices_to_screen(self, modelview, projection, viewport):
        screen_coords = []
        for vertex in self.vertices:
            projected = gluProject(vertex[0], vertex[1], vertex[2], modelview, projection, viewport)
            screen_coords.append(projected[:2])
        return screen_coords

    def contains_point(self, x, y, modelview, projection, viewport):
        screen_coords = self.project_vertices_to_screen(modelview, projection, viewport)
        if not screen_coords:
            return False
        min_x = min(coord[0] for coord in screen_coords)
        max_x = max(coord[0] for coord in screen_coords)
        min_y = min(coord[1] for coord in screen_coords)
        max_y = max(coord[1] for coord in screen_coords)
        return min_x <= x <= max_x and min_y <= y <= max_y


fovy_min, fovy_max = 30, 150
aspect_min, aspect_max = 4. / 3., 21. / 9.
z_near_min, z_near_max = 0.1, 10
z_far_min, z_far_max = 10, 1000


class Camera:
    def __init__(self, position, target, up_vector, pitch=0, yaw=270, fovy=PERSPECTIVE_ANGLE,
             aspect=WINDOW_WIDTH / WINDOW_HEIGHT, z_near=NEAR_CLIP, z_far=FAR_CLIP):
        self.position = np.array(position, dtype=np.float32)
        self.target = np.array(target, dtype=np.float32)
        self.up_vector = np.array(up_vector, dtype=np.float32)
        self.pitch = pitch  # Up and down rotation (vertical)
        self.yaw = yaw  # Left and right rotation (horizontal)
        self.fovy = fovy
        self.aspect = aspect
        self.z_near = z_near
        self.z_far = z_far


    def apply_transformations(self):
        gluLookAt(self.position[0], self.position[1], self.position[2],
                  self.target[0], self.target[1], self.target[2],
                  self.up_vector[0], self.up_vector[1], self.up_vector[2])


    def rotate(self, dx, dy, dz=0):
        self.yaw -= dy
        self.pitch += dx
        # Limit the pitch to avoid flipping the camera
        self.pitch = max(-89.0, min(89.0, self.pitch))

        # Calculate new direction vector based on yaw and pitch
        direction = np.array([
            math.cos(math.radians(self.yaw)) * math.cos(math.radians(self.pitch)),
            math.sin(math.radians(self.pitch)),
            math.sin(math.radians(self.yaw)) * math.cos(math.radians(self.pitch))
        ], dtype=np.float32)

        # Update the target position
        self.target = self.position + direction


    def translate(self, x, y, z):
        translation_vector = np.array([x, y, z], dtype=np.float32)
        self.position += translation_vector
        self.target += translation_vector


    def update_fovy(self, delta_fovy=0):
        self.fovy = max(fovy_min, min(fovy_max, self.fovy + delta_fovy))


    def update_aspect(self, delta_aspect):
        if not delta_aspect:
            return
        self.aspect = delta_aspect
        self.aspect = max(aspect_min, min(aspect_max, delta_aspect))  # Ensures aspect ratio within plausible boundaries

    def update_z_near(self, delta_z_near):
        self.z_near = max(z_near_min, min(z_near_max, self.z_near + delta_z_near))  # Clamps the near clip plane distance

    def update_z_far(self, delta_z_far):
        self.z_far = max(z_far_min, min(z_far_max, self.z_far + delta_z_far))  # Clamps the far clip plane distance


    def get_perspective(self):
        return self.fovy, self.aspect, self.z_near, self.z_far


class Scene:
    def __init__(self):
        self.figures = []
        self.camera: Camera = None
        self.selected_figure: Figure3D = None
        self.is_rotating = False
        self.last_mouse_x = 0
        self.last_mouse_y = 0

    def add_figure(self, figure):
        self.figures.append(figure)

    def set_camera(self, camera):
        self.camera = camera

    def deselect_figure(self):
        if self.selected_figure is not None:
            self.selected_figure.selected = False
            self.selected_figure = None

    def select_figure(self, figure):
        figure.selected = True
        self.selected_figure = figure

    def handle_click(self, x, y, button):
        if button == GLUT_LEFT_BUTTON:
            window_width = glutGet(GLUT_WINDOW_WIDTH)
            window_height = glutGet(GLUT_WINDOW_HEIGHT)
            viewport = glGetIntegerv(GL_VIEWPORT)
            modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
            projection = glGetDoublev(GL_PROJECTION_MATRIX)
            self.deselect_figure()
            for figure in self.figures:
                if figure.contains_point(x, window_height - y - 1, modelview, projection, viewport):
                    self.select_figure(figure)
                    break

    def handle_motion(self, x, y):
        if self.is_rotating and self.camera:
            # Update the camera with the movement difference
            dx = x - self.last_mouse_x
            dy = y - self.last_mouse_y
            sensitivity = 0.1  # adjust sensitivity as needed
            self.camera.rotate(dy * sensitivity, dx * sensitivity)

            self.last_mouse_x = x
            self.last_mouse_y = y
        glutPostRedisplay()

    def draw(self):
        if self.camera:
            self.camera.apply_transformations()
        for figure in self.figures:
            figure.draw()


scene = Scene()
camera = Camera([0, 0, 5], [0, 0, 0], [0, 1, 0])
scene.set_camera(camera)

cube_vertices = [
    [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],
    [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]
]
cube_edges = [(0, 1), (1, 2), (2, 3), (3, 0),
              (4, 5), (5, 6), (6, 7), (7, 4),
              (0, 4), (1, 5), (2, 6), (3, 7)]
cube_faces = [
    (0, 1, 2, 3), (4, 5, 6, 7),
    (0, 1, 5, 4), (2, 3, 7, 6),
    (0, 3, 7, 4), (1, 2, 6, 5)
]
cube = Figure3D(cube_vertices, cube_edges, cube_faces, color=(0, 1, 0))

pyramid_vertices = [
    [0, 1, 0], [-1, -1, -1], [1, -1, -1],
    [1, -1, 1], [-1, -1, 1]
]
pyramid_edges = [(0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (2, 3), (3, 4), (4, 1)]
pyramid_faces = [(0, 1, 2), (0, 2, 3), (0, 3, 4), (0, 4, 1), (1, 2, 3, 4)]
pyramid = Figure3D(pyramid_vertices, pyramid_edges, pyramid_faces, color=(1, 0, 0), draw_mode='faces')
pyramid.translate(3, 0, 0)

sphere_vertices = [
    [-1, 0, 0], [1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]
]
sphere_edges = [
    (0, 1), (2, 3), (4, 5)
]
sphere_faces = [
    (0, 1, 2), (3, 4, 5)
]
sphere = Figure3D(sphere_vertices, sphere_edges, sphere_faces, color=(0, 0, 1), draw_mode='edges')
sphere.translate(-3, 0, 0)

scene.add_figure(cube)
scene.add_figure(pyramid)
scene.add_figure(sphere)


def display():
    # glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # glLoadIdentity()
    # scene.draw()
    # glutSwapBuffers()
    scene.render()


def reshape(width, height):
    if height == 0:
        height = 1
    glViewport(0, 0, width, height)
    if scene.camera:
        scene.camera.update_aspect(width / height)  # Update aspect ratio
        scene.camera.set_perspective()
    # glMatrixMode(GL_PROJECTION)
    # glLoadIdentity()
    # scene.camera.update_aspect(width / height)
    # gluPerspective(scene.camera.fovy, scene.camera.aspect, scene.camera.z_near, scene.camera.z_far)
    # glMatrixMode(GL_MODELVIEW)
    # fovy, aspect, z_near, z_far = scene.camera.get_perspective()
    # gluPerspective(fovy, aspect, z_near, z_far)
    # glMatrixMode(GL_MODELVIEW)
timer = 0


def reset_perspective():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    fov = scene.camera.fovy if scene.camera else 45.0
    aspect = glutGet(GLUT_WINDOW_WIDTH) / max(glutGet(GLUT_WINDOW_HEIGHT), 1)
    z_near = scene.camera.z_near if scene.camera else 1.0
    z_far = scene.camera.z_far if scene.camera else 50.0
    gluPerspective(fov, aspect, z_near, z_far)
    glMatrixMode(GL_MODELVIEW)

def display():
    global timer
    timer +=1
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    scene.draw()
    glutSwapBuffers()


def reshape(width, height):
    if height == 0:
        height = 1
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    fov = scene.camera.fovy if scene.camera else 45.
    aspect = width / height if width and height else 1.5
    z_near = scene.camera.z_near if scene.camera else 1.
    z_far = scene.camera.z_far if scene.camera else 50.
    gluPerspective(fov, aspect, z_near, z_far)
    glMatrixMode(GL_MODELVIEW)

def set_draw_mode(draw_mode):
    if scene.selected_figure:
        scene.selected_figure.set_draw_mode(draw_mode)
    else:
        for figure in scene.figures:
            figure.set_draw_mode(draw_mode)


def translate_figure_or_camera(x, y, z):
    if scene.selected_figure:
        scene.selected_figure.translate(x, y, z)
    else:
        camera.translate(x, y, z)


def rotate_figure_or_camera(dx, dy, dz):
    if scene.selected_figure:
        scene.selected_figure.rotate(dx, dy, dz)
    else:
        camera.rotate(dx, dy, dz)


def change_camera_perspective(delta_fovy, aspect, delta_z_near, delta_z_far):
    if delta_z_far is not None:
        camera.update_z_far(delta_z_far)
    if delta_fovy is not None:
        camera.update_fovy(delta_fovy)
    if aspect is not None:
        camera.update_aspect(aspect)
    if delta_z_near is not None:
        camera.update_z_near(delta_z_near)
    reset_perspective()

pressed_keys = OrderedSet()


def special_keyboard_up(key, x, y):
    str_key = glut_keys_modifiers.get(key)
    if str_key:
        keyboard_up(str_key, x, y)


def special_keyboard(key, x, y):
    str_key = glut_keys_modifiers.get(key)
    if str_key:
        keyboard(str_key, x, y)


def keyboard_up(key, x, y):
    global pressed_keys
    if isinstance(key, bytes):
        try:
            key = key.decode('utf-8')
        except UnicodeDecodeError:
            # TODO add other languages support
            return
    pressed_keys.discard(key)


glut_keys_modifiers = {
    27: 'esc',
    32: 'enter',
    b'\x1b': 'esc',
    b'\x03': 'ctrl+c',
    b'\x20': 'enter',
    GLUT_KEY_F1: "f1",
    GLUT_KEY_F2: "f2",
    GLUT_KEY_F3: "f3",
    GLUT_KEY_F4: "f4",
    GLUT_KEY_F5: "f5",
    GLUT_KEY_F6: "f6",
    GLUT_KEY_F7: "f7",
    GLUT_KEY_F8: "f8",
    GLUT_KEY_F9: "f9",
    GLUT_KEY_F10: "f10",
    GLUT_KEY_F11: "f11",
    GLUT_KEY_F12: "f12",
    GLUT_KEY_LEFT: "left",
    GLUT_KEY_UP: "up",
    GLUT_KEY_RIGHT: "right",
    GLUT_KEY_DOWN: "down",
    GLUT_KEY_PAGE_UP: "page up",
    GLUT_KEY_PAGE_DOWN: "page down",
    GLUT_KEY_HOME: "home",
    GLUT_KEY_END: "end",
    GLUT_KEY_INSERT: "insert",
    GLUT_ACTIVE_SHIFT: "shift",
    GLUT_ACTIVE_CTRL: "ctrl",
    GLUT_ACTIVE_ALT: "alt",
    112: "shift",
    114: "ctrl",
    116: "alt",
}

action_values = {
    'draw_points': {
        'action': set_draw_mode,
        'args': ('points',)
    },
    'draw_edges': {
        'action': set_draw_mode,
        'args': ('edges',)
    },
    'draw_faces': {
        'action': set_draw_mode,
        'args': ('faces',)
    },
    'translate_left': {
        'action': translate_figure_or_camera,
        'args': (-0.5, 0, 0)
    },
    'translate_right': {
        'action': translate_figure_or_camera,
        'args': (0.5, 0, 0)
    },
    'translate_forward': {
        'action': translate_figure_or_camera,
        'args': (0, 0, -0.5)
    },
    'translate_backward': {
        'action': translate_figure_or_camera,
        'args': (0, 0, 0.5)
    },
    'translate_up': {
        'action': translate_figure_or_camera,
        'args': (0, 0.5, 0)
    },
    'translate_down': {
        'action': translate_figure_or_camera,
        'args': (0, -0.5, 0)
    },
    'rotate_x_plus': {
        'action': rotate_figure_or_camera,
        'args': (0, -5, 0)
    },
    'rotate_x_minus': {
        'action': rotate_figure_or_camera,
        'args': (0, 5, 0)
    },
    'rotate_y_plus': {
        'action': rotate_figure_or_camera,
        'args': (5, 0, 0)
    },
    'rotate_y_minus': {
        'action': rotate_figure_or_camera,
        'args': (-5, 0, 0)
    },
    'increase_render_distance': {
        'action': change_camera_perspective,
        'args': (None, None, None, +10.)
    },
    'decrease_render_distance': {
        'action': change_camera_perspective,
        'args': (None, None, None, -10.)
    },
    'zoom_up': {
        'action': change_camera_perspective,
        'args': (-5., None, None, None)
    },
    'zoom_down': {
        'action': change_camera_perspective,
        'args': (5., None, None, None)
    },
    'exit': {
        'action': glutLeaveMainLoop,
        'args': ()
    }
}


def execute_command(action_key):
    command = action_values.get(action_key)
    if not command:
        return
    action = command.get('action')
    args = command.get('args')
    action(*args)


def int_to_bit_powers(n):
    result = []
    power = 0
    while n > 0:
        if n & 1:
            result.append(2 ** power)
        n >>= 1
        power += 1
    return result


SHIFT = GLUT_ACTIVE_SHIFT
CTRL = GLUT_ACTIVE_CTRL
ALT = GLUT_ACTIVE_ALT
SHIFT_CTRL = SHIFT | CTRL
SHIFT_ALT = SHIFT | ALT
CTRL_ALT = CTRL | ALT
SHIFT_CTRL_ALT = SHIFT | CTRL | ALT

# Create the main dictionary with integer keys for each modifier combination
shortcuts = {
    SHIFT: {
        '+': 'zoom_up',
        '-': 'zoom_down',
    },
    CTRL: {
    },
    ALT: {
    },
    SHIFT_CTRL: {
    },
    SHIFT_ALT: {
    },
    CTRL_ALT: {
    },
    SHIFT_CTRL_ALT: {
    }
}

action_keys = {
    '1': 'draw_points',
    '2': 'draw_edges',
    '3': 'draw_faces',
    'a': 'translate_left',
    'd': 'translate_right',
    'w': 'translate_forward',
    's': 'translate_backward',
    'r': 'translate_up',
    'f': 'translate_down',
    '+': 'increase_render_distance',
    '-': 'decrease_render_distance',
    'right': 'rotate_x_plus',
    'left': 'rotate_x_minus',
    'up': 'rotate_y_plus',
    'down': 'rotate_y_minus',
    'esc': 'exit',
}


def keyboard(key, x, y):
    global pressed_keys
    if isinstance(key, bytes):
        try:
            key = key.decode('utf-8')
        except UnicodeDecodeError:
            # TODO add other languages support
            return
    key.lower()
    pressed_keys.add(key)
    print(f"Pressed keys: {pressed_keys}")

    modifiers = glutGetModifiers()

    def handle_actions():
        for pressed_key in pressed_keys:
            # Check for action with modifier or without
            if modifiers:
                action_name = shortcuts.get(modifiers).get(pressed_key)
                if not action_name:
                    continue
                execute_command(action_name)
                break
            if pressed_key not in action_keys.keys():
                continue
            action_name = action_keys.get(pressed_key)
            execute_command(action_name)

    handle_actions()
    glutPostRedisplay()


def mouse(button, state, x, y):
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        scene.handle_click(x, y, button)
    elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        scene.is_rotating = True
        scene.last_mouse_x = x
        scene.last_mouse_y = y
    elif button == GLUT_RIGHT_BUTTON and state == GLUT_UP:
        scene.is_rotating = False
    elif button == GLUT_MIDDLE_BUTTON:
        print("Change perspective")
        gluPerspective((x + y) % 180, 4. / 3., 1., 1000.)
    glutPostRedisplay()

def wheel(wheel, direction, x, y):
    if direction > 0:
        execute_command('zoom_up')
    else:
        execute_command('zoom_down')
    glutPostRedisplay()


def motion(x, y):
    scene.handle_motion(x, y)


def init_glut():
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

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    # Uncomment if you need special key handling
    # glutSpecialFunc(special_keyboard)
    # glutSpecialUpFunc(special_keyboard_up)
    glutKeyboardFunc(keyboard)
    glutKeyboardUpFunc(keyboard_up)
    glutMouseFunc(mouse)
    glutMotionFunc(motion)

    glutMainLoop()


def init_glut():
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

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    # Uncomment if you need special key handling
    glutSpecialFunc(special_keyboard)
    glutSpecialUpFunc(special_keyboard_up)
    glutKeyboardFunc(keyboard)
    glutKeyboardUpFunc(keyboard_up)
    glutMouseFunc(mouse)
    glutMotionFunc(motion)
    glutMouseWheelFunc(wheel)
    glutMainLoop()


if __name__ == "__main__":
    init_glut()

