from v1.engine.util.quaternion import Quaternion
from v1.engine.util.vector3d import Vector3D


class Component:
    """ ID of component """
    id: int

    """ Unique name of component """
    name: str

    """ 3D size of object in km """
    size: Vector3D

    """ Position of component in km """
    position: Vector3D

    """ Actual rotational position of component (referenced: origin) """
    rotation: Quaternion

    def __init__(self, name: str, size: Vector3D, position: Vector3D, rotation: Quaternion = Quaternion(1, 0, 0, 0)):
        self.name = name
        self.size = size
        self.position = position
        self.rotation = rotation
