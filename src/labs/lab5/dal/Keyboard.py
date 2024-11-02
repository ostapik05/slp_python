from OpenGL.GLUT import *

SHIFT = GLUT_ACTIVE_SHIFT
CTRL = GLUT_ACTIVE_CTRL
ALT = GLUT_ACTIVE_ALT
SHIFT_CTRL = SHIFT | CTRL
SHIFT_ALT = SHIFT | ALT
CTRL_ALT = CTRL | ALT
SHIFT_CTRL_ALT = SHIFT | CTRL | ALT

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

glut_keys_modifiers = {
    27: 'esc',
    32: 'enter',
    '\x1b': 'esc',
    '\x03': 'ctrl+c',
    '\x20': 'enter',
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