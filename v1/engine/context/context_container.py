from typing import Type, TypeVar

from v1.engine.context.context import Context


CType = TypeVar('CType', bound=Context)


class ContextContainer:
    """ State storage across listeners """

    container: dict[str, Context] = {}

    def get(self, ctype: Type[CType]) -> CType:
        return self.container[str(ctype)]

    def add(self, c: Context):
        if str(type(c)) in self.container:
            raise KeyError(f'Context "{type(c)}" already exists')

        self.container[str(type(c))] = c

    def remove(self, c: Context):
        del self.container[str(type(c))]
