class CameraData:
    def __init__(self, position = [0, 0, 0], target =[0, 0, -1],
                 up_vector =[0, 1, 0], pitch: float = 0.0, yaw: float = 0.0,
                 fovy: float = 45.0, aspect: float = 1.33, z_near: float = 0.1, z_far: float = 1000.0):
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
