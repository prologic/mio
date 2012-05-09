from mio import runtime
from mio.utils import method

from mio.object import Object


from list import List


class Map(Object):

    def __init__(self, value={}):
        super(Map, self).__init__(value=value)

        self.create_methods()
        self["parent"] = runtime.state.find("Object")

    def __iter__(self):
        for item in self.value.items():
            yield List(item)

    def __str__(self):
        pairs = ", ".join(["%s: %r" % (k, v) for k, v in self.value.items()])
        return "{%s}" % pairs

    @method()
    def init(self, receiver, context, m, *args):
        it = iter(args)
        self.value = dict(list(zip(it, it)))

    # General Operations

    @method()
    def clear(self, receiver, context, m):
        self.value.clear()
        return runtime.state.find("None")

    @method()
    def copy(self, receiver, context, m):
        return self.clone(self.value.copy())

    @method()
    def get(self, receiver, context, m, key, default=None):
        return self.value.get(key, default)

    @method()
    def has(self, receiver, context, m, key):
        if key in self.value:
            return runtime.state.find("True")
        return runtime.state.find("False")

    @method()
    def items(self, receiver, context, m):
        items = [List(item) for item in self.value.items()]
        return List(items)

    @method()
    def keys(self, receiver, context, m):
        return List(self.value.keys())

    @method()
    def set(self, receiver, context, m, key, value):
        self.value[key] = value
        return self

    @method()
    def values(self, receiver, context, m):
        return List(self.value.values())
