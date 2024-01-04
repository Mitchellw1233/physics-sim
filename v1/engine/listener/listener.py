from abc import abstractmethod

from v1.engine.component.component import Component
from v1.engine.context.context_container import ContextContainer


class Listener:
    context: ContextContainer

    def __init__(self, context: ContextContainer):
        self.context = context

    def start(self, c: Component):
        """ Executed once per component on start of simulation """
        pass

    def loop_single_before(self):
        """ Executed once per frame, before loop, no component attached """
        pass

    def loop_single_after(self):
        """ Executed once per frame, after loop, no component attached """
        pass

    def loop(self, c: Component):
        """ Executed once per component per frame """
        pass

    @staticmethod
    @abstractmethod
    def should_listen(c: Component) -> bool:
        """ Decides if it should be assigned to component """
        pass
