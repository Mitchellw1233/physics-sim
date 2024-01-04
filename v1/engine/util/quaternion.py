from math import atan2, asin, cos, sin

from v1.engine.util.angle3d import Angle3D


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

    @staticmethod
    def from_euler_angles(euler: Angle3D):
        cx = cos(euler.x / 2)
        sx = sin(euler.x / 2)
        cy = cos(euler.y / 2)
        sy = sin(euler.y / 2)
        cz = cos(euler.z / 2)
        sz = sin(euler.z / 2)

        return Quaternion(
            cx * cy * cz - sx * sy * sz,
            sx * cy * cz + cx * sy * sz,
            cx * sy * cz - sx * cy * sz,
            cx * sy * cz + sx * sy * cz,
        )
