from abc import abstractmethod

from v1.engine.component.component import Component


class Storage:
    """ Storage class for storing simulation data """

    name: str

    """ Interval for writing to file, in between its storing in memory """
    store_interval: int

    """ Temp frames stored in memory """
    temp_frames: list[dict[int, Component]] = []

    def __init__(self, name: str, store_interval: int):
        self.name = name
        self.store_interval = store_interval

    def append(self, frame: dict[int, Component]):
        self.temp_frames.append(frame)

        if len(self.temp_frames) % self.store_interval == 0:
            self.store()

    @abstractmethod
    def read(self) -> list[dict[int]]:  # TODO: TypedDict or serialization (could be tricky if object changes)?
        pass

    @abstractmethod
    def store(self):
        pass
