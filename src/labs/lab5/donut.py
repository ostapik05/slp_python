import os
import time
from math import cos, sin
import pygame
import colorsys

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
hue = 0

os.environ['SDL_VIDEO_CENTERED'] = '1'
RES = WIDTH, HEIGHT = 700, 700
FPS = 60
# Figure position
figure_x, figure_y = WIDTH // 2, HEIGHT // 2

pixel_width = 20
pixel_height = 20

x_pixel = 0
y_pixel = 0

screen_width = WIDTH // pixel_width
screen_height = HEIGHT // pixel_height
screen_size = screen_width * screen_height

A, B = 0, 0

theta_spacing = 10
# theta_spacing = 15
phi_spacing = 3
# phi_spacing = 4

chars = ".,-~:;=!*#$@"

R1 = 10
R2 = 40
K2 = 400
K1 = screen_height * K2 * 3 / (8 * (R1 + R2))

pygame.init()

screen = pygame.display.set_mode(RES)
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 20, bold=True)
position_change_modes = ['rotating', 'transitioning']
ROTATING_MODE = position_change_modes[0]
TRANSITIONING_MODE = position_change_modes[1]
position_change_mode = ROTATING_MODE
speed = 0.01  # Initial hue change speed


def hsv2rgb(h, s, v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h, s, v))


def text_display(char, x, y):
    text = font.render(str(char), True, hsv2rgb(hue, 1, 1))
    text_rect = text.get_rect(center=(x, y))
    screen.blit(text, text_rect)


k = 0

paused = False
running = True
writed = []
while running:
    clock.tick(FPS)
    pygame.display.set_caption("FPS: {:.2f}".format(clock.get_fps()))
    screen.fill(BLACK)

    output = [' '] * screen_size
    zbuffer = [0] * screen_size

    # Calculate dynamic theta_spacing and phi_spacing based on distance (K2) and resolution (screen_size).
    resolution_factor = (screen_width + screen_height) / 2#50
    theta_spacing = max(2, int(1000 / resolution_factor))  # Ensuring a minimum spacing of 2
    phi_spacing = max(2, int(100 / resolution_factor))
    for theta in range(0, 628, theta_spacing):  # theta goes around the cross-sectional circle of a torus, from 0 to 2pi
        for phi in range(0, 628, phi_spacing):  # phi goes around the center of revolution of a torus, from 0 to 2pi

            cosA = cos(A)
            sinA = sin(A)
            cosB = cos(B)
            sinB = sin(B)

            costheta = cos(theta)
            sintheta = sin(theta)
            cosphi = cos(phi)
            sinphi = sin(phi)

            # x, y coordinates before revolving
            circlex = R2 + R1 * costheta

            circley = R1 * sintheta

            # 3D (x, y, z) coordinates after rotation
            x = circlex * (cosB * cosphi + sinA * sinB * sinphi) - circley * cosA * sinB
            y = circlex * (sinB * cosphi - sinA * cosB * sinphi) + circley * cosA * cosB
            z = K2 + cosA * circlex * sinphi + circley * sinA
            if z == 0:
                continue
            ooz = 1 / z  # one over z

            # x, y projection
            xp = int(figure_x / pixel_width + K1 * ooz * x)
            yp = int(figure_y / pixel_height - K1 * ooz * y)

            if 0 <= xp < screen_width and 0 <= yp < screen_height:
                position = (xp + screen_width * yp) % screen_size

                # luminance (L ranges from -sqrt(2) to sqrt(2))
                L = cosphi * costheta * sinB - cosA * costheta * sinphi - sinA * sintheta + cosB * (
                        cosA * sintheta - costheta * sinA * sinphi)

                if ooz > zbuffer[position]:
                    zbuffer[
                        position] = ooz  # larger ooz means the pixel is closer to the viewer than what's already plotted
                    luminance_index = int(
                        L * 8)  # we multiply by 8 to get luminance_index range 0..11 (8 * sqrt(2) = 11)
                    output[position] = chars[luminance_index if luminance_index > 0 else 0]

    for i in range(screen_height):
        y_pixel += pixel_height
        for j in range(screen_width):
            x_pixel += pixel_width
            text_display(output[k], x_pixel, y_pixel)
            k += 1
        x_pixel = 0
    y_pixel = 0
    k = 0

    # Update rotation angles
    # A += 0.15  # Commenting out to stop the spinning
    # B += 0.035  # Commenting out to stop the spinning
    # hue += 0.005

    # Check for user input to adjust rotation
    keys = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pressed()
    wheel = pygame.event.get(pygame.MOUSEWHEEL)
    focused = pygame.mouse.get_focused()
    # print(mouse)
    if keys[pygame.K_UP]:
        A -= 0.05
    if keys[pygame.K_DOWN]:
        A += 0.05
    if keys[pygame.K_LEFT]:
        B -= 0.05
    if keys[pygame.K_RIGHT]:
        B += 0.05
    if keys[pygame.K_w]:
        figure_y -= 5
    if keys[pygame.K_s]:
        figure_y += 5
    if keys[pygame.K_a]:
        figure_x -= 5
    if keys[pygame.K_d]:
        figure_x += 5
    if wheel:
        wheel = wheel[0]
        print(wheel.y)
        K2 += wheel.y*35
    if keys[pygame.K_t]:
        position_change_mode = TRANSITIONING_MODE
    if keys[pygame.K_r]:
        position_change_mode = ROTATING_MODE
    mouse_motion = pygame.mouse.get_rel()
    if focused:
        if mouse[0]:
            # print(mouse_motion)
            # print(f"A: {A}, B: {B}")
            A -= mouse_motion[0] * 0.005
            B -= mouse_motion[1] * 0.005
            # print(f"A: {A}, B: {B}")
        if mouse[2]:
            print(pygame.mouse.get_rel())
    if keys[pygame.K_c]:
        hue += speed

    if hue > 1:
        hue = 0

    # Check for user input to adjust figure position
    if position_change_mode == ROTATING_MODE:
        pass
    elif position_change_mode == TRANSITIONING_MODE:
        pass
    else:
        raise ValueError("Invalid position_change_mode")
    if not paused:
        pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_SPACE:
                paused = not paused
