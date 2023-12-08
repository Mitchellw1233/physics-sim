import json
import os.path

from v1.engine.component.component import Component


class JSONStorage:
    path: str

    def __init__(self, path: str):
        self.path = path

    def read(self) -> list[dict[int, Component]] | None:
        if not os.path.exists(self.path):
            return None

        return json.load(open(self.path, 'r'))

    def store(self, frame: dict[id, Component]):
        with open(self.path, 'x') as f:
            content = json.load(f)
            if content == '':
                content = []
            if not isinstance(content, list):
                raise TypeError(f'File "{self.path}" does not contain right format')

            content.append(frame)
            json.dump(content, f)
