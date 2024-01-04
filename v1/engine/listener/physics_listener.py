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

    collision_pos_events = {'x': {}, 'y': {}, 'z': {}}

    def start(self, c: PhysicalComponent):
        pass

    def loop_single_before(self):
        # Reset history
        self.gravity_history = {}

    def loop_single_after(self):
        self._collision_single()
        self.collision_pos_events = {'x': {}, 'y': {}, 'z': {}}

    # Can safely assume PhysicalComponent because of should_listen()
    def loop(self, c: PhysicalComponent):
        time_s = Settings.delta / 1000  # Time in seconds

        self._collision_loop(c)

        # Time complexity: O(n**2 / 2)
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
        c.velocity += a * time_s

        # Reset force
        c.net_force = 0

        # Translate velocity to position
        c.position = c.position + (c.velocity * time_s)

        # Add component to history
        self.gravity_history[c.id] = None

    @staticmethod
    def should_listen(c: Component) -> bool:
        return isinstance(c, PhysicalComponent)

    def _compute_gravity(self, c: PhysicalComponent, other: PhysicalComponent):
        # Calculate gravity, very accurate but very inefficient
        #   TODO: better use The Barnes-Hut Algorithm, but tiny loss in accuracy
        # Right now O(n**2), but we continue if checked, so heavy computation is O(n**2 / 2)
        # n = number of PhysicalComponents

        # Calculate translation and distance with a minimum of 1 to avoid division errors
        #   and should be physically impossible, because it would attract more than it's mass allows
        pos_diff = other.position - c.position
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

    def _collision_loop(self, c: PhysicalComponent):
        # Largest possible radius for colliding
        radius = math.sqrt(c.size.x ** 2 + c.size.y ** 2 + c.size.z) / 2

        # define start and end position of component for each axes
        self.collision_pos_events['x'].setdefault(c.position.x - radius, []).append((1, c.id))
        self.collision_pos_events['x'].setdefault(c.position.x + radius, []).append((-1, c.id))

        self.collision_pos_events['y'].setdefault(c.position.y - radius, []).append((1, c.id))
        self.collision_pos_events['y'].setdefault(c.position.y + radius, []).append((-1, c.id))

        self.collision_pos_events['z'].setdefault(c.position.z - radius, []).append((1, c.id))
        self.collision_pos_events['z'].setdefault(c.position.z + radius, []).append((-1, c.id))

    def _collision_single(self):
        """ Checking for possible collisions and sends them to _collision_detect """
        # TODO: No continuous collision detection yet, maybe implement later?
        context = self.context.get(SimulationContext)

        # Possible collisions per axes
        poss_coll_axial = {'x': {}, 'y': {}, 'z': {}}

        # Loop through events and check for possible collisions per axes
        for axial in self.collision_pos_events:
            active_components = set()
            for pos in sorted(self.collision_pos_events[axial].keys()):
                for c_meta in self.collision_pos_events[axial][pos]:
                    event_type = c_meta[0]
                    cid = c_meta[1]

                    # If -1, end of component
                    if event_type == -1:
                        active_components.remove(cid)
                        continue

                    # Start of component
                    for active_id in active_components:
                        poss_coll_axial[axial][f'{active_id}+{cid}'] = True  # Possible collision detected
                    active_components.add(cid)

        # poss_coll_axial only checks per axes, so check if possible collision is present for all 3 axes,
        # if so: inpect actual mesh to see if collision is occuring, or will occur.
        for k in poss_coll_axial['x']:
            if k not in poss_coll_axial['y'] or k not in poss_coll_axial['z']:
                continue

            cids = k.split('+')
            # should be a physical component
            # noinspection PyTypeChecker
            self._collision_detect(context.get_component(int(cids[0])), context.get_component(int(cids[1])))

    def _collision_detect(self, c1: PhysicalComponent, c2: PhysicalComponent):
        # TODO: When mesh implemented detect accurately
        print(f'{c1.name} & {c2.name} possible collision')

    def _collision_handle(self, c1: PhysicalComponent, c2: PhysicalComponent):
        # TODO: Maybe merge with collision detect, as it probs contains information this function needs to act on
        pass
