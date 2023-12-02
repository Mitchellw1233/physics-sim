from v1.engine.component.component import Component
from v1.engine.component.physical_component import PhysicalComponent
from v1.engine.listener.listener import Listener
from v1.engine.settings import Settings


class PhysicsListener(Listener):
    def start(self, c: PhysicalComponent):
        pass

    def loop_single(self):
        pass

    # Can safely assume PhysicalComponent because of should_listen()
    def loop(self, c: PhysicalComponent):
        time = Settings.delta / 1000
        c.position = c.position + (c.velocity * time)

    @staticmethod
    def should_listen(c: Component) -> bool:
        return isinstance(c, PhysicalComponent)
