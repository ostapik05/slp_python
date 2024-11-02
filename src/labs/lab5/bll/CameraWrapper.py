import numpy as np
from OpenGL.GLU import gluLookAt
import math
from labs.lab5.config import *
from labs.lab5.dal.Camera import CameraData





class Camera:
    def __init__(self, data=None):
        self.data = data

    def set_data(self, data):
        if data:
            self.data = data

    @classmethod
    def create(cls, position, target, up_vector, pitch=0, yaw=270, fovy=PERSPECTIVE_ANGLE,
               aspect=WINDOW_WIDTH / WINDOW_HEIGHT, z_near=NEAR_CLIP, z_far=FAR_CLIP):
        data = CameraData(
            position=np.array(position, dtype=np.float32),
            target=np.array(target, dtype=np.float32),
            up_vector=np.array(up_vector, dtype=np.float32),
            pitch=pitch,
            yaw=yaw,
            fovy=fovy,
            aspect=aspect,
            z_near=z_near,
            z_far=z_far
        )
        instance = cls(data)
        return instance

    def apply_transformations(self):
        gluLookAt(self.data.position[0], self.data.position[1], self.data.position[2],
                  self.data.target[0], self.data.target[1], self.data.target[2],
                  self.data.up_vector[0], self.data.up_vector[1], self.data.up_vector[2])

    def rotate(self, dx, dy, dz=0):
        self.data.yaw -= dy
        self.data.pitch += dx
        # Limit the pitch to avoid flipping the camera
        self.data.pitch = max(-89.0, min(89.0, self.data.pitch))

        # Calculate new direction vector based on yaw and pitch
        direction = np.array([
            math.cos(math.radians(self.data.yaw)) * math.cos(math.radians(self.data.pitch)),
            math.sin(math.radians(self.data.pitch)),
            math.sin(math.radians(self.data.yaw)) * math.cos(math.radians(self.data.pitch))
        ], dtype=np.float32)

        # Update the target position
        self.data.target = self.data.position + direction

    def translate(self, x, y, z):
        translation_vector = np.array([x, y, z], dtype=np.float32)
        self.data.position += translation_vector
        self.data.target += translation_vector

    def update_fovy(self, delta_fovy=0):
        self.data.fovy = max(fovy_min, min(fovy_max, self.data.fovy + delta_fovy))

    def update_aspect(self, delta_aspect):
        if not delta_aspect:
            return
        self.data.aspect = delta_aspect
        self.data.aspect = max(aspect_min,
                               min(aspect_max, delta_aspect))  # Ensures aspect ratio within plausible boundaries

    def update_z_near(self, delta_z_near):
        self.data.z_near = max(z_near_min,
                               min(z_near_max, self.data.z_near + delta_z_near))  # Clamps the near clip plane distance

    def update_z_far(self, delta_z_far):
        self.data.z_far = max(z_far_min,
                              min(z_far_max, self.data.z_far + delta_z_far))  # Clamps the far clip plane distance

    def get_perspective(self):
        return self.data.fovy, self.data.aspect, self.data.z_near, self.data.z_far

