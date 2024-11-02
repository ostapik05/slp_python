import numpy as np
from labs.lab5.config import *


class CameraData:
    def __init__(self, position: np.ndarray = default_position, target: np.ndarray = default_target,
                 up_vector: np.ndarray = default_up_vector, pitch: float = default_pitch, yaw: float = default_yaw,
                 fovy: float = default_fovy, aspect: float = default_aspect, z_near: float = default_z_near,
                 z_far: float = default_z_far):
        self.position = position
        self.target = target
        self.up_vector = up_vector
        self.pitch = pitch
        self.yaw = yaw
        self.fovy = fovy
        self.aspect = aspect
        self.z_near = z_near
        self.z_far = z_far

    def __repr__(self):
        return f"CameraData(position={self.position}, target={self.target}, up_vector={self.up_vector}, pitch={self.pitch}, yaw={self.yaw}, fovy={self.fovy}, aspect={self.aspect}, z_near={self.z_near}, z_far={self.z_far})"

    def __eq__(self, other):
        if not isinstance(other, CameraData):
            return NotImplemented
        return (np.array_equal(self.position, other.position) and
                np.array_equal(self.target, other.target) and
                np.array_equal(self.up_vector, other.up_vector) and
                self.pitch == other.pitch and
                self.yaw == other.yaw and
                self.fovy == other.fovy and
                self.aspect == self.aspect and
                self.z_near == other.z_near and
                self.z_far == other.z_far)
