from __future__ import annotations
from typing import TYPE_CHECKING

from v1.engine.component.component import Component
from v1.engine.context.context import Context

if TYPE_CHECKING:
    from v1.engine.simulation import Simulation


class SimulationContext(Context):
    sim: Simulation

    def __init__(self, sim: Simulation):
        self.sim = sim

    def get_component(self, identifier: int) -> Component:
        """ Get component by id """
        return self.sim.env[identifier]

    def get_component_by_name(self, name: str) -> Component:
        """ Get component by name """
        return self.sim.env[self.sim.components_by_name[name]]

    def get_components(self) -> dict[int, Component]:
        return self.sim.env
