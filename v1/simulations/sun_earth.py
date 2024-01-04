import math

from v1.engine.component.physical_component import PhysicalComponent
from v1.engine.settings import Settings
from v1.engine.simulation import Simulation
from v1.engine.storage.csv_storage import CSVStorage
from v1.engine.util.angle3d import Angle3D
from v1.engine.util.quaternion import Quaternion
from v1.engine.util.vector3d import Vector3D
from v1.rendering.blender_renderer import BlenderRenderer


Settings.fps = 30
Settings.delta = 1000 * 60 * 30  # 1s * 60 * 30 = 30min
# simulated time/s = delta * fps = 900min/s (15h/s)
Settings.frame_limit = int(365.25 * 86400000 / Settings.delta)  # 1 year (in ms divided by delta)

# BlenderRenderer(Settings.fps, Settings.frame_limit)
name = 'sun_earth'
sim = Simulation(
    [],
    [],
    renderer=BlenderRenderer(Settings.fps, Settings.frame_limit, name),
    # storage=CSVStorage(name, 10000),
)

sim.add_component(PhysicalComponent(
    name='sun',
    position=Vector3D.zero(),
    mass=1.9885e+30,
    size=Vector3D(1392000000, 1392000000, 1392000000),
    rotation=Quaternion.from_euler_angles(Angle3D.from_degrees(7.25, 0, 0)),
    angular_velocity=Angle3D(0, 0, 1.997e6),
))
sim.add_component(PhysicalComponent(
    name='earth',
    size=Vector3D(12756000, 12756000, 12756000),
    position=Vector3D(0, -147098074000, 0),
    mass=5.972e+24,
    velocity=Vector3D(30290, 0, 0),
    c_drag=0.3,
))

if __name__ == '__main__':
    sim.setup()
    sim.start()
    # i = 0
    # print('Loading frames..')
    # for frame in sim.storage.read_as_objects():
    #     i += 1
    #
    # print(f'loaded {i} frames as objects')
