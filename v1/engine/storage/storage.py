import os.path
from abc import abstractmethod
from typing import Generator

from root import base_dir
from v1.engine.component.component import Component
from v1.engine.util.helper import from_fqn


class Storage:
    """ Storage class for storing simulation data """

    name: str
    path: str

    """ Interval for writing to file, in between its storing in memory """
    store_interval: int

    """ Temp rows and iterations stored in memory """
    temp_data: list[object] = []
    temp_iterations: list[int] = []

    def __init__(self, name: str, store_interval: int):
        self.name = name
        self.path = os.path.join(base_dir(), 'data', name)
        self.store_interval = store_interval

    def append(self, data: object, iteration: int):
        self.temp_data.append(data)
        self.temp_iterations.append(iteration)

        if len(self.temp_data) % self.store_interval == 0:
            self.save()

    @abstractmethod
    def read(self) -> Generator[object, None, None]:
        pass

    @abstractmethod
    def read_as_objects(self) -> Generator[object, None, None]:
        pass

    @abstractmethod
    def save(self):
        pass

    @staticmethod
    def decode_recursive(obj, max_depth: int = 9):
        if max_depth == 0:
            return obj

        # If a list, recursive
        if isinstance(obj, list):
            return [Storage.decode_recursive(item, max_depth - 1) for item in obj]

        # If not a dict or list, return itself
        if not isinstance(obj, dict):
            return obj

        # Assume dict
        # If contains _fqn, assume its a class
        if '_fqn' in obj:
            return from_fqn(obj['_fqn'])(**{
                k: Storage.decode_recursive(obj[k], max_depth - 1) for k in obj if k != '_fqn'
            })

        # else normal dict
        return {k: Storage.decode_recursive(obj[k], max_depth - 1) for k in obj}
