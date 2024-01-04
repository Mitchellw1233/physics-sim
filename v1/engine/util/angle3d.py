from __future__ import annotations

import math
from v1.engine.util.vector3d import Vector3D


class Angle3D(Vector3D):
    """ Angles in radians (can be converted to degrees) """
    _degrees: Vector3D = None

    def __init__(self, x: float, y: float, z: float):
        super().__init__(x, y, z)
        # self.degrees = self._generate_deg()

    # def __setattr__(self, key, value):
    #     if key in ['x', 'y', 'z']:
    #         self.__dict__[key] = value
    #         self.degrees.__dict__[key] = self.x * (180 / math.pi)
    #         return
    #
    #     self.__dict__[key] = value

    def degrees(self):
        return Angle3D(
            self.x * (180 * math.pi),
            self.y * (180 * math.pi),
            self.z * (180 * math.pi)
        )

    @staticmethod
    def from_degrees(x: float, y: float, z: float) -> Angle3D:
        return Angle3D(
            x * math.pi / 180,
            y * math.pi / 180,
            z * math.pi / 180,
        )

    # def _generate_deg(self):
    #     return Vector3D(
    #         self.x * (180 * math.pi),
    #         self.y * (180 * math.pi),
    #         self.z * (180 * math.pi)
    #     )
