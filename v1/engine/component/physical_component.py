from math import atan2

from v1.engine.component.component import Component
from v1.engine.util.angle3d import Angle3D
from v1.engine.util.quaternion import Quaternion
from v1.engine.util.vector3d import Vector3D


class PhysicalComponent(Component):
    """ Physical component """

    """ Mass in kg """
    mass: float

    """ Force in Newton, resetted every frame for now """
    net_force: Vector3D  # TODO: Not sure about this, no info about where the exact force is applied.
    # Maybe list[{force: float, direction: Angle3D, location: Vector3D (from component origin)}] or something

    """ Center of Mass (reference: component origin) """
    com: Vector3D

    """ Center of Pressure (reference: component origin) """
    cop: Vector3D

    """ Velocity in m/s (reference: origin) """
    velocity: Vector3D

    """ Angular velocity in radians per second (reference: component origin) """
    angular_velocity: Angle3D

    """ float | { x: { y: { z: float } }} known drag coefficient(s) pointing in certain direction angles (x, y, z) """
    c_drag: float | dict[float, dict[float, dict[float, float]]]  # TODO: interpolate between angles when we need drag efficiently

    # TODO: Fluid/gas passing through could maybe simply be simulated by having a fluid data class in component.
    #       Instead of defining fluid areas with complicated math to simulate earth atmosphere for example
    #       For example: passing_fluid could be implemented here with dynamic properties which change over position
    #           (altitude). So density, relative_direction or absolute_direction, relative_velocity or abs_velocity etc

    def __init__(self,
                 mass: float,
                 net_force: Vector3D = Vector3D(0, 0, 0),
                 com: Vector3D = Vector3D(0, 0, 0),
                 cop: Vector3D = Vector3D(0, 0, 0),
                 velocity: Vector3D = Vector3D(0, 0, 0),
                 angular_velocity: Angle3D = Angle3D(0, 0, 0),
                 c_drag: float | dict[float, dict[float, dict[float, float]]] = 0,
                 *args,
                 **kwargs
                 ):
        super().__init__(*args, **kwargs)

        self.mass = mass
        self.net_force = net_force
        self.com = com
        self.cop = cop
        self.velocity = velocity
        self.angular_velocity = angular_velocity
        self.c_drag = c_drag

    def direction(self) -> Angle3D:
        x_abs = abs(self.velocity.x)
        y_abs = abs(self.velocity.y)
        z_abs = abs(self.velocity.z)

        return Angle3D(
            atan2(
                self.velocity.y if y_abs > z_abs else z_abs,
                self.velocity.x
            ),
            atan2(
                self.velocity.x if x_abs > z_abs else z_abs,
                self.velocity.y
            ),
            atan2(
                self.velocity.x if x_abs > y_abs else y_abs,
                self.velocity.z
            ),
        )

    def aoa(self) -> Angle3D:
        return self.rotation.euler_angles() - self.direction()
