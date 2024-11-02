from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from labs.lab5.config import *
from PIL import Image
import numpy as np

ascii_chars = "@%#*+=-:. "
color_palette = [
    (0.0, 0.0, 0.0),  # Black
    (0.1, 0.1, 0.1),  # Dark Gray
    (0.2, 0.2, 0.2),  # Gray
    (0.5, 0.5, 0.5),  # Light Gray
    (0.7, 0.7, 0.7),  # Lighter Gray
    (0.9, 0.9, 0.9),  # Near White
    (1.0, 1.0, 1.0),  # White
]


def map_pixel_to_ascii(gray_value, color_value):
    scale = gray_value / 255
    char = ascii_chars[int(scale * (len(ascii_chars) - 1))]
    r, g, b = color_value
    return f"\033[38;2;{r};{g};{b}m{char}\033[0m"

def render_to_ascii(width, height, scale_ratio):
    glReadBuffer(GL_FRONT)
    pixels = glReadPixels(0, 0, width, height, GL_RGB, GL_UNSIGNED_BYTE)
    image = Image.frombytes("RGB", (width, height), pixels)

    scaled_width = int(width * scale_ratio)
    scaled_height = int(height * scale_ratio * 0.25)
    image = image.resize((scaled_width, scaled_height), Image.NEAREST)


    grayscale_image = image.convert('L')
    color_image = np.array(image)

    pixel_data = np.array(grayscale_image)

    ascii_image = []
    for row, color_row in zip(pixel_data[::-1], color_image[::-1]):
        ascii_row = ''.join(map(map_pixel_to_ascii, row, color_row))
        ascii_image.append(ascii_row)

    return '\n'.join(ascii_image)



def display(scene_draw_callback):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    scene_draw_callback()
    ascii_art = render_to_ascii(WINDOW_WIDTH, WINDOW_HEIGHT, ASCII_SCALE_RATIO)
    print(ascii_art)
    glutSwapBuffers()


def reshape(width, height, fov, aspect, z_near, z_far):
    if height == 0:
        height = 1
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fov, aspect, z_near, z_far)
    glMatrixMode(GL_MODELVIEW)
