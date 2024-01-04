import random

from v1.engine.component.physical_component import PhysicalComponent
from v1.engine.settings import Settings
from v1.engine.simulation import Simulation
from v1.engine.util.vector3d import Vector3D
from v1.rendering.blender_renderer import BlenderRenderer

Settings.fps = 30
Settings.delta = 1000 * 60  # 1s * 60 = 1min
# simulated time/s = delta * fps = 900min/s (15h/s)
Settings.frame_limit = int(2 * 86400000 / Settings.delta)  # 10days in ms (divided by delta)

name = 'n_earth'
sim = Simulation(
    [],
    [],
    renderer=BlenderRenderer(Settings.fps, Settings.frame_limit, name),
    # storage=CSVStorage(name, 10000),
)

for i in range(int(20)):
    print(i)
    # TODO: Very slow with dicts because of hash collisions. Change to list structure and make deletion of object
    #       O(n) or alternatively just make None, but not the best idea
    sim.add_component(PhysicalComponent(
        name=f'earth-{i:06d}',
        size=Vector3D(12756000, 12756000, 12756000),
        position=Vector3D(
            random.randint(0, 20) * 15000000,
            random.randint(0, 20) * 15000000,
            random.randint(0, 10) * 15000000,
        ),
        mass=5.972e+24,
        velocity=Vector3D(
            random.randint(-20, 20),
            random.randint(-20, 20),
            random.randint(-20, 20),
        ),
        c_drag=0.3,
    ))

if __name__ == '__main__':
    sim.setup()
    sim.start()
