from mio.utils import Null
from mio.object import Object
from mio.pymethod import pymethod


class Map(Object):

    @pymethod()
    def init(self, value=Null):
        if value is Null:
            self.value = {}
        else:
            self.value = dict(value)

    # General Operations

    @pymethod()
    def clear(self):
        self.value.clear()
        return self.lobby("None")

    @pymethod()
    def copy(self):
        return self.clone(self.value.copy())

    @pymethod()
    def get(self, key, default=None):
        return self.value.get(key, default)

    @pymethod()
    def has(self, key):
        test = key in self.value
        return self.lobby("True") if test else self.lobby("False")

    @pymethod()
    def items(self):
        List = self.lobby("List")
        items = [List.clone(item) for item in self.value.items()]
        return List.clone(items)

    @pymethod()
    def keys(self):
        return self.lobby("List").clone(self.value.keys())

    @pymethod()
    def set(self, key, value):
        self.value[key] = value
        return value

    @pymethod()
    def values(self):
        return self.lobby("List").clone(self.value.values())

    # Boolean Operations

    @pymethod()
    def lt(self, other):
        test = self.value < other.value
        return self.lobby("True") if test else self.lobby("False")

    @pymethod()
    def gt(self, other):
        test = self.value > other.value
        return self.lobby("True") if test else self.lobby("False")

    # Type Conversion

    @pymethod()
    def repr(self):
        pairs = ", ".join(["%s=%s" % (k, v) for k, v in self.value.items()])
        return self.lobby("String").clone("Map(%s)" % pairs)
