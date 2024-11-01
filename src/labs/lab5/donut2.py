import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

class Figure3D:
    def __init__(self, vertices, edges, faces=None, color=(1, 1, 1), draw_mode='edges'):
        self.vertices = np.array(vertices, dtype=np.float32)
        self.edges = edges
        self.faces = faces if faces is not None else []
        self.color = color
        self.angle = [0, 0, 0]
        self.draw_mode = draw_mode
        self.selected = False

    def rotate(self, axis, angle):
        center = np.mean(self.vertices, axis=0)
        self.translate(-center[0], -center[1], -center[2])

        # Виконуємо обертання відносно вибраної осі
        angle_rad = math.radians(angle)
        rotation_matrix = np.identity(3)
        if axis == 'x':
            rotation_matrix = np.array([
                [1, 0, 0],
                [0, math.cos(angle_rad), -math.sin(angle_rad)],
                [0, math.sin(angle_rad), math.cos(angle_rad)]
            ])
        elif axis == 'y':
            rotation_matrix = np.array([
                [math.cos(angle_rad), 0, math.sin(angle_rad)],
                [0, 1, 0],
                [-math.sin(angle_rad), 0, math.cos(angle_rad)]
            ])
        elif axis == 'z':
            rotation_matrix = np.array([
                [math.cos(angle_rad), -math.sin(angle_rad), 0],
                [math.sin(angle_rad), math.cos(angle_rad), 0],
                [0, 0, 1]
            ])

        self.vertices = np.dot(self.vertices, rotation_matrix.T)
        self.translate(center[0], center[1], center[2])
        self.angle[{"x": 0, "y": 1, "z": 2}[axis]] += angle

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
            screen_coords.append(projected[:2])  # We only need X and Y
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


class Camera:
    def __init__(self, position, target, up_vector):
        self.position = np.array(position, dtype=np.float32)
        self.target = np.array(target, dtype=np.float32)
        self.up_vector = np.array(up_vector, dtype=np.float32)
        self.angle = [0, 0, 0]
        self.target_still = False

    def apply_transformations(self):
        gluLookAt(self.position[0], self.position[1], self.position[2],
                  self.target[0], self.target[1], self.target[2],
                  self.up_vector[0], self.up_vector[1], self.up_vector[2])

    def rotate(self, axis, angle):
        angle_rad = math.radians(angle)
        if not self.target_still:
            direction = self.target - self.position
        else:
            direction = self.target

        if axis == 'x':
            rotation_matrix = np.array([
                [1, 0, 0],
                [0, math.cos(angle_rad), -math.sin(angle_rad)],
                [0, math.sin(angle_rad), math.cos(angle_rad)]
            ])
        elif axis == 'y':
            rotation_matrix = np.array([
                [math.cos(angle_rad), 0, math.sin(angle_rad)],
                [0, 1, 0],
                [-math.sin(angle_rad), 0, math.cos(angle_rad)]
            ])
        elif axis == 'z':
            rotation_matrix = np.array([
                [math.cos(angle_rad), -math.sin(angle_rad), 0],
                [math.sin(angle_rad), math.cos(angle_rad), 0],
                [0, 0, 1]
            ])

        new_direction = np.dot(direction, rotation_matrix.T)

        if not self.target_still:
            self.target = self.position + new_direction

    def translate(self, x, y, z):
        translation_matrix = np.array([x, y, z], dtype=np.float32)
        self.position += translation_matrix
        if not self.target_still:
            self.target += translation_matrix

    def apply_transformations(self):
        gluLookAt(self.position[0], self.position[1], self.position[2],
                  self.target[0], self.target[1], self.target[2],
                  self.up_vector[0], self.up_vector[1], self.up_vector[2])

    def rotate(self, dx, dy):
        # Calculate horizontal (dx) rotation around the Y axis
        rotation_matrix_y = np.array([
            [math.cos(math.radians(dx)), 0, math.sin(math.radians(dx))],
            [0, 1, 0],
            [-math.sin(math.radians(dx)), 0, math.cos(math.radians(dx))]
        ])

        # Calculate vertical (dy) rotation around the X axis
        rotation_matrix_x = np.array([
            [1, 0, 0],
            [0, math.cos(math.radians(dy)), -math.sin(math.radians(dy))],
            [0, math.sin(math.radians(dy)), math.cos(math.radians(dy))]
        ])

        direction = self.target - self.position
        new_direction = np.dot(rotation_matrix_x, np.dot(rotation_matrix_y, direction))

        self.target = self.position + new_direction

class Camera:
    def __init__(self, position, target, up_vector):
        self.position = np.array(position, dtype=np.float32)
        self.target = np.array(target, dtype=np.float32)
        self.up_vector = np.array(up_vector, dtype=np.float32)
        self.angle = [0, 0, 0]

    def apply_transformations(self):
        gluLookAt(self.position[0], self.position[1], self.position[2],
                  self.target[0], self.target[1], self.target[2],
                  self.up_vector[0], self.up_vector[1], self.up_vector[2])

    def rotate(self, dx, dy):
        # Calculate horizontal (dx) rotation around the Y axis
        rotation_matrix_y = np.array([
            [math.cos(math.radians(dx)), 0, math.sin(math.radians(dx))],
            [0, 1, 0],
            [-math.sin(math.radians(dx)), 0, math.cos(math.radians(dx))]
        ])

        # Calculate vertical (dy) rotation around the X axis
        rotation_matrix_x = np.array([
            [1, 0, 0],
            [0, math.cos(math.radians(dy)), -math.sin(math.radians(dy))],
            [0, math.sin(math.radians(dy)), math.cos(math.radians(dy))]
        ])

        direction = self.target - self.position
        new_direction = np.dot(rotation_matrix_x, np.dot(rotation_matrix_y, direction))

        self.target = self.position + new_direction

    def translate(self, x, y, z):
        translation_vector = np.array([x, y, z], dtype=np.float32)
        self.position += translation_vector
        self.target += translation_vector


class Scene:
    def __init__(self):
        self.figures = []
        self.camera = None
        self.selected_figure = None
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
        elif button == GLUT_RIGHT_BUTTON:
            if self.selected_figure is not None:
                self.is_rotating = True
                self.last_mouse_x = x
                self.last_mouse_y = y

    def handle_motion(self, x, y):
        if self.selected_figure is not None and self.is_rotating:
            dx = x - self.last_mouse_x
            dy = y - self.last_mouse_y
            self.selected_figure.rotate('y', dx)
            self.selected_figure.rotate('x', dy)
            self.last_mouse_x = x
            self.last_mouse_y = y

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
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    scene.draw()
    glutSwapBuffers()


def reshape(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, width / height, 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)


pressed_keys = set()
action_keys = {
    b'1': 'draw_points',
    b'2': 'draw_edges',
    b'3': 'draw_faces',
    b't': 'target_still',
    b'a': 'translate_left',
    b'd': 'translate_right',
    b'w': 'translate_forward',
    b's': 'translate_backward',
    b'r': 'translate_up',
    b'f': 'translate_down',
    b'7': 'rotate_x_plus',
    b'4': 'rotate_x_minus',
    b'8': 'rotate_y_plus',
    b'5': 'rotate_y_minus',
    b'9': 'rotate_z_plus',
    b'6': 'rotate_z_minus'
}

action_values = {
    'draw_points': {'mode': 'points'},
    'draw_edges': {'mode': 'edges'},
    'draw_faces': {'mode': 'faces'},
    'target_still': {'name': 'Target still'},
    'translate_left': {'x': -0.5, 'y': 0, 'z': 0},
    'translate_right': {'x': 0.5, 'y': 0, 'z': 0},
    'translate_forward': {'x': 0, 'y': 0, 'z': -0.5},
    'translate_backward': {'x': 0, 'y': 0, 'z': 0.5},
    'translate_up': {'x': 0, 'y': 0.5, 'z': 0},
    'translate_down': {'x': 0, 'y': -0.5, 'z': 0},
    'rotate_x_plus': {'axis': 'x', 'angle': 5},
    'rotate_x_minus': {'axis': 'x', 'angle': -5},
    'rotate_y_plus': {'axis': 'y', 'angle': 5},
    'rotate_y_minus': {'axis': 'y', 'angle': -5},
    'rotate_z_plus': {'axis': 'z', 'angle': 5},
    'rotate_z_minus': {'axis': 'z', 'angle': -5}
}

def keyboard_up(key, x, y):
    global pressed_keys
    pressed_keys.discard(key)


def keyboard(key, x, y):
    global pressed_keys
    pressed_keys.add(key)

    def handle_actions():

        for pressed_key in pressed_keys:
            if not pressed_key in action_keys:
                continue
            name = action_keys[pressed_key]
            if 'draw_' in name:
                if scene.selected_figure:
                    scene.selected_figure.set_draw_mode(action_values[name]['mode'])
                else:
                    for figure in scene.figures:
                        figure.set_draw_mode(action_values[name]['mode'])
            elif 'translate_' in name:
                if scene.selected_figure:
                    scene.selected_figure.translate(**action_values[name])
                else:
                    camera.translate(**action_values[name])
            elif 'rotate_' in name:
                if scene.selected_figure:
                    scene.selected_figure.rotate(**action_values[name])
                else:
                    camera.rotate(**action_values[name])
            elif name:
                scene.camera.target_still = not scene.camera.target_still

    handle_actions()
    glutPostRedisplay()


def mouse(button, state, x, y):
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        scene.handle_click(x, y, button)
    elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        scene.handle_click(x, y, button)
    elif button == GLUT_RIGHT_BUTTON and state == GLUT_UP:
        scene.is_rotating = False
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
    glutPostRedisplay()

def motion(x, y):
    scene.handle_motion(x, y)
    glutPostRedisplay()


def init_glut():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH | GLUT_STENCIL)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"3D Scene with PyOpenGL")
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_STENCIL_TEST)
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutKeyboardUpFunc(keyboard_up)
    glutMouseFunc(mouse)
    glutMotionFunc(motion)
    glutMainLoop()


if __name__ == "__main__":
    init_glut()