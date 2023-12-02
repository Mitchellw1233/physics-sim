from typing import TypedDict, Type

from v1.engine.component.component import Component
from v1.engine.component.physical_component import PhysicalComponent
from v1.engine.context.context import Context
from v1.engine.context.context_container import ContextContainer
from v1.engine.context.simulation_context import SimulationContext
from v1.engine.listener.listener import Listener
from v1.engine.listener.physics_listener import PhysicsListener
from v1.rendering.renderer import Renderer


class ComponentMeta(TypedDict):
    listeners: list[int]


class Simulation:
    """ Simulation """

    renderer: Renderer
    run: bool = False

    """ Environment containing all items
    { component_id: Component }
    """
    env: dict[int, Component] = {}

    """ { component_id: ComponentMeta } """
    components_meta: dict[int, ComponentMeta] = {}

    """ Listeners
    { id: Listener }
    """
    listeners: dict[int, Listener] = {}

    # Mappers / categorizes
    """ Component ids mapped by name
        { name: component_id }
    """
    components_by_name: dict[str, int] = {}

    """ list[component_id] """
    physical_components: list[int] = []

    # Other
    context_container: ContextContainer

    def __init__(self, renderer: Renderer, listeners: list[Type[Listener]], contexts: list[Context]):
        self.renderer = renderer

        # Setup context container
        self.context_container = ContextContainer()
        self.context_container.add(SimulationContext(self))
        for c in contexts:
            self.context_container.add(c)

        # Setup listeners
        self.listeners[0] = PhysicsListener(self.context_container)
        for i in range(len(listeners)):
            self.listeners[i] = listeners[i](self.context_container)

    def setup(self):
        # Setup environment: categorize physical components and assign right listeners to components
        for cid in self.env:
            if isinstance(self.env[cid], PhysicalComponent):
                self.physical_components.append(cid)

            for lid in self.listeners:
                if self.listeners[lid].should_listen(self.env[cid]):
                    self.components_meta[cid]['listeners'].append(lid)

        self.renderer.setup(self.env)

    def start(self):
        self.run = True
        for cid in self.env:
            for lid in self.components_meta[cid]['listeners']:
                self.listeners[lid].start(self.env[cid])

        while self.run is True:
            self.loop()

    def loop(self):
        # TODO: does order matter?
        # Execute single loop per listener
        for lid in self.listeners:
            self.listeners[lid].loop_single()

        # For each component, execute the loop of its listeners
        for cid in self.env:
            for lid in self.components_meta[cid]['listeners']:
                self.listeners[lid].loop(self.env[cid])

        # Render/visualize next frame
        self.renderer.render_frame(self.env)
        self.renderer.next_frame()

    def stop(self):
        self.run = False

    def add_component(self, c: Component):
        c.id = list(self.env)[-1] + 1 if len(self.env) > 0 else 0

        if c.name in self.components_by_name:
            raise KeyError(f'Name "{c.name}" already exists')

        if isinstance(c, PhysicalComponent):
            self.physical_components.append(c.id)

        listener_ids = []
        for lid in self.listeners:
            if self.listeners[lid].should_listen(c):
                listener_ids.append(lid)

        self.env[c.id] = c
        self.components_meta[c.id] = {'listeners': listener_ids}
        self.renderer.add_component(c)

    def remove_component(self, component: int | str):
        cid = component
        cname = component

        if isinstance(component, str):
            cid = self.components_by_name[component]
        else:
            cname = self.env[component].name

        del self.env[cid]
        del self.components_meta[cid]
        del self.components_by_name[cname]
        self.renderer.remove_component(self.env[cid])