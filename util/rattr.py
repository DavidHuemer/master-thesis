import functools


def rgetattr(obj, attr, *args):
    def _getattr(obj1, attr1):
        return getattr(obj1, attr1, *args)

    return functools.reduce(_getattr, [obj] + attr.split('.'))
