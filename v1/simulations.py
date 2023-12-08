import math

from v1.engine.component.physical_component import PhysicalComponent
from v1.engine.util.angle3d import Angle3D
from v1.engine.util.quaternion import Quaternion
from v1.engine.util.vector3d import Vector3D

sun_earth = {
    'fps': 30,
    'frame_limit': int(1e6),
    'components': [
        PhysicalComponent(
            name='sun',
            position=Vector3D.zero(),
            mass=3.955e+30,  # 5.972e+24
            size=Vector3D(1392000, 1392000, 1392000),
            rotation=Quaternion.from_euler_angles(Angle3D(7.25 * math.pi/180, 0, 0)),  # TODO: sun is angled
            angular_velocity=Angle3D(0, 0, 1.997e6),
        ),
        PhysicalComponent(
            name='earth',
            size=Vector3D(12756, 12756, 12756),
            position=Vector3D(),
            mass=5.972e+24,
            velocity=Vector3D(random.randint(-50, 50), random.randint(-50, 50), random.randint(-50, 50)),
            c_drag=0.3,
        ),
    ],
}
