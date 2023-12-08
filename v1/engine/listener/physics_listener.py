import math

from v1.engine.component.component import Component
from v1.engine.component.physical_component import PhysicalComponent
from v1.engine.context.simulation_context import SimulationContext
from v1.engine.listener.listener import Listener
from v1.engine.settings import Settings
from v1.engine.util.vector3d import Vector3D


class PhysicsListener(Listener):
    G: float = 6.67430e-11
    gravity_history: dict[int, None] = {}  # Dict for better performance

    def start(self, c: PhysicalComponent):
        pass

    def loop_single(self):
        # print('======== Frame ========')
        # Reset history
        self.gravity_history = {}

    # Can safely assume PhysicalComponent because of should_listen()
    def loop(self, c: PhysicalComponent):
        # print(f'LOOP: {c.id}-{c.name}')
        time_s = Settings.delta / 1000  # Time in seconds

        # Calculate gravity, very accurate but very inefficient
        #   TODO: better use The Barnes-Hut Algorithm, but tiny loss in accuracy
        # Right now O(n**2), but we continue if checked, so heavy computation is O(n**2 / 2)
        # n = number of PhysicalComponents
        sim_context = self.context.get(SimulationContext)
        for other_cid in sim_context.get_components():
            if other_cid in self.gravity_history or other_cid == c.id:
                continue  # Already calculated or itself

            other = sim_context.get_component(other_cid)
            if not isinstance(other, PhysicalComponent):
                continue  # No gravity for non-physical components

            self._compute_gravity(c, other)

        # Translate force to acceleration, calculate velocity and add it to velocity
        a = c.net_force / c.mass
        # print(f'{c.id}-{c.name}:')
        # print(f'    force: {c.net_force.__dict__}')
        # print(f'    pos: {c.position.__dict__}')
        # for t in test:
        #     print(t)
        # print(f'    pre-velocity: {c.velocity.__dict__}')
        # print(f'    force_velocity: {(a * time_s).__dict__}')
        c.velocity += a * time_s
        # print(f'    post-velocity: {c.velocity.__dict__}')

        # Reset force
        c.net_force = 0

        # Translate velocity to position
        c.position = c.position + (c.velocity * time_s / 1000)

        # Add component to history
        self.gravity_history[c.id] = None

    @staticmethod
    def should_listen(c: Component) -> bool:
        return isinstance(c, PhysicalComponent)

    def _compute_gravity(self, c: PhysicalComponent, other: PhysicalComponent):
        # Calculate translation and distance (converted to meters) with a minimum of 1 to avoid devision errors
        #   and should be physically impossible, because it would attract more than it's mass allows
        pos_diff = (other.position - c.position) * 1000
        distance = math.sqrt(pos_diff.x ** 2 + pos_diff.y ** 2 + pos_diff.z ** 2)
        limited_distance = max(1.0, distance)

        # Calculate gravitational force
        gravity_force = self.G * c.mass * other.mass / limited_distance ** 2

        # Add force to component. If distance is 0, we have a force that's equal in every axes
        if distance != 0:
            force: Vector3D = gravity_force / distance * pos_diff
            c.net_force += force
            other.net_force += -force
            return

        # TODO: Rework: @see PhysicalComponent.net_force comment
        # Distance == 0, so we calculate net force by checking if gravity force is stronger than current net force
        # If so, we can simply put 0 as the object does not have enough to overcome gravity force
        # If not, we subtract the gravity_force and the leftover force will be the force applied
        def _calculate_force(net_force: float):
            if gravity_force > abs(net_force):
                return 0

            # Leftover force between net_force and gravity_force in direction of net_force, therefore gravity_force is
            # converted to - or + to align with net_force (with copysign)
            return net_force - gravity_force * math.copysign(1, net_force)

        # Apply forces
        c.net_force = Vector3D(
            _calculate_force(c.net_force.x),
            _calculate_force(c.net_force.y),
            _calculate_force(c.net_force.z)
        )
        other.net_force = Vector3D(
            _calculate_force(other.net_force.x),
            _calculate_force(other.net_force.y),
            _calculate_force(other.net_force.z)
        )
