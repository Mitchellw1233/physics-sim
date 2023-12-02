from typing import Type

from v1.engine.context.context import Context


class ContextContainer:
    """ State storage across listeners """

    container: dict[str, Context] = {}

    def get(self, ctype: Type[Context]) -> Context:
        return self.container[str(ctype)]

    def add(self, c: Context):
        print(self.container)
        print(str(type(c)) in self.container)
        if str(type(c)) in self.container:
            raise KeyError(f'Context "{type(c)}" already exists')

        self.container[str(type(c))] = c

    def remove(self, c: Context):
        del self.container[str(type(c))]
