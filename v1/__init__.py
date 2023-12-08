import random

from v1.engine.component.component import Component
from v1.engine.component.physical_component import PhysicalComponent
from v1.engine.settings import Settings
from v1.engine.simulation import Simulation
from v1.engine.util.vector3d import Vector3D
from v1.rendering.blender_renderer import BlenderRenderer

# TODO: Maybe rework listener, performance wise not smart to assign per Component for physics_listener
#       Goal is to have O(n) instead of O(n**2). O(n**2) is when we loop through components and in physics_listener
#       Loop through all Components again for example.
#       Find a good way to have listeners on multiple components at once maybe?
#           Maybe we need to be able to access another listener (which is higher up for example)?
#           Then we could use that information of the bigger manager one in normal listener, but still wouldn't work i
#           think, because we would loop n amount in the higher, and n amount for all smaller listeners.
#       Or can we keep structure somehow?
# TODO: Use FBX ?

if __name__ == '__main__':
    sim = Simulation(BlenderRenderer(Settings.fps, Settings.frame_limit), [], [])

    for i in range(int(20)):
        print(i)
        # TODO: Very slow with dicts because of hash collisions. Change to list structure and make deletion of object
        #       O(n) or alternatively just make None, but not the best idea
        sim.add_component(PhysicalComponent(
            name=f'earth-{i:06d}',
            size=Vector3D(12756, 12756, 12756),
            position=Vector3D(random.randint(0, 20) * 15000, random.randint(0, 20) * 15000, random.randint(0, 10) * 15000),
            mass=5.972e+24,
            velocity=Vector3D(random.randint(-50, 50), random.randint(-50, 50), random.randint(-50, 50)),
            c_drag=0.3,
        ))

        # sim.add_component(PhysicalComponent(
        #     name=f'earth-{i:06d}',
        #     size=Vector3D(12756, 12756, 12756),
        #     position=Vector3D(i * 15000, 0, 0),
        #     mass=5.972e+24,
        #     net_force=Vector3D(0, 0, 0),
        #     velocity=Vector3D(0, 0, 0),
        #     c_drag=0.3,
        # ))

    sim.setup()
    sim.start()
