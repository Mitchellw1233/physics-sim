from math import atan2, asin, pi

from v1.engine.util.angle3d import Angle3D
from v1.engine.util.vector3d import Vector3D


class Quaternion:
    w: float
    x: float
    y: float
    z: float

    def __init__(self, w: float, x: float, y: float, z: float):
        self.w = w
        self.x = x
        self.y = y
        self.z = z

    def euler_angles(self) -> Angle3D:
        """euler angles in radians"""
        return Angle3D(
            atan2(2 * (self.w * self.x + self.y * self.z), 1 - 2 * (self.x ** 2 + self.y ** 2)),
            asin(2 * (self.w * self.y - self.z * self.x)),
            atan2(2 * (self.w * self.z + self.x * self.y), 1 - 2 * (self.y ** 2 + self.z ** 2))
        )
