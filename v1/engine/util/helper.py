import importlib


def to_fqn(obj):
    cls = type(obj)
    module = cls.__module__
    name = cls.__qualname__
    if module is None or module == '__builtin__':
        return name

    return module + '.' + name


def from_fqn(fqn: str):
    components = fqn.split('.')

    if len(components) < 2:
        return globals()[fqn]

    module_path = '.'.join(components[:-1])
    class_name = components[-1]

    # importlib.import_module(module_path)
    return getattr(__import__(module_path, fromlist=[class_name]), class_name)
