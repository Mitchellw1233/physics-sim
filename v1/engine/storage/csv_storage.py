import csv
import json
import os

from v1.engine.component.component import Component
from v1.engine.storage.storage import Storage
from v1.engine.util.helper import to_fqn


class CSVStoreIterator:
    def __init__(self, temp_data: list[object], temp_iterations: list[int]):
        self._data = temp_data
        self._iterations = temp_iterations
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index >= len(self._data):
            raise StopIteration

        # 26s for 180 000 frames
        # item = [self._index, pickle.dumps(self._temp_frames[self._index], pickle.HIGHEST_PROTOCOL)]

        # 24.3s for 180 000 frames
        # serializable = []
        # for cid in self._temp_frames[self._index]:
        #     serializable.append({
        #         'type': type(self._temp_frames[self._index][cid]).__name__,
        #         'component': self._temp_frames[self._index][cid]
        #     })
        # TODO: Maybe using pickle to store dicts instead of classes. Could be faster, but does probs not differ much
        #       test with loads en dumps pickle vs json for million dicts = 2.77s for json, 0.44s for pickle.
        #       But json uses **__dict__ which cannot be used with pickle, therefore it has to preprocess the data first
        #       and may affect performance
        item = [
            str(self._iterations[self._index]),
            json.dumps(self._data[self._index], default=lambda o: {'_fqn': to_fqn(o), **o.__dict__}),
        ]

        # 22.46s for 180 000 frames
        # item = [self._index, json.dumps(self._temp_frames[self._index], default=lambda o: o.__dict__)]
        self._index += 1
        return item


class CSVStorage(Storage):
    def __init__(self, name: str, store_interval: int):
        super().__init__(name, store_interval)
        self.path += '.csv'

        if os.path.isfile(self.path):
            os.remove(self.path)

    def read(self):
        if not os.path.isfile(self.path):
            raise FileNotFoundError()

        f = open(self.path, 'r')
        reader = csv.reader(f, delimiter=';')
        next(reader)  # Skip headers
        for row in reader:
            yield json.loads(row[1])

    def read_as_objects(self):
        for item in self.read():
            yield Storage.decode_recursive(item)

    def save(self):
        print(f'Saving {len(self.temp_data)} row(s) to "{self.path}"..')
        file_exists = os.path.isfile(self.path)
        f = open(self.path, 'a')
        writer = csv.writer(f, delimiter=';', lineterminator='\n')

        if not file_exists:
            writer.writerow(['iteration', 'data'])

        writer.writerows(CSVStoreIterator(self.temp_data, self.temp_iterations))
        f.close()
        self.temp_data = []
        self.temp_iterations = []
        print('Saved!')
