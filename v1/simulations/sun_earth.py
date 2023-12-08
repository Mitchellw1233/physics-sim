import math

from v1.engine.component.physical_component import PhysicalComponent
from v1.engine.settings import Settings
from v1.engine.simulation import Simulation
from v1.engine.util.angle3d import Angle3D
from v1.engine.util.quaternion import Quaternion
from v1.engine.util.vector3d import Vector3D
from v1.rendering.blender_renderer import BlenderRenderer
from v1.rendering.renderer import Renderer

Settings.fps = 30
Settings.delta = 1000 * 60 * 30  # 30min * fps = 900min per seconde
Settings.frame_limit = 30*60 * 10


sim = Simulation(BlenderRenderer(Settings.fps, Settings.frame_limit), [], [])
sim.add_component(PhysicalComponent(
    name='sun',
    position=Vector3D.zero(),
    mass=1.9885e+30,
    size=Vector3D(1392000, 1392000, 1392000),
    rotation=Quaternion.from_euler_angles(Angle3D(7.25 * math.pi / 180, 0, 0)),  # TODO: sun is angled
    angular_velocity=Angle3D(0, 0, 1.997e6),
))
sim.add_component(PhysicalComponent(
    name='earth',
    size=Vector3D(12756, 12756, 12756),
    position=Vector3D(0, -147098074, 0),
    mass=5.972e+24,
    velocity=Vector3D(30290, 0, 0),
    c_drag=0.3,
))

if __name__ == '__main__':
    sim.setup()
    sim.start()
