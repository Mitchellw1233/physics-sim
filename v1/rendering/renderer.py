from abc import abstractmethod

from v1.engine.component.component import Component


class Renderer:
    fps: int
    frame_limit: int
    name: str

    def __init__(self, fps: int, frame_limit: int, name: str):
        self.fps = fps
        self.frame_limit = frame_limit
        self.name = name

    @abstractmethod
    def setup(self, frame: dict[int, Component]):
        pass

    @abstractmethod
    def render_frame(self, frame: dict[int, Component]):
        pass

    @abstractmethod
    def next_frame(self):
        pass

    @abstractmethod
    def save(self):
        pass

    @abstractmethod
    def add_component(self, c: Component):
        pass

    @abstractmethod
    def remove_component(self, c: Component):
        pass
