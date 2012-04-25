from mio.utils import Null
from mio.object import Object
from mio.pymethod import pymethod


class List(Object):

    @pymethod()
    def init(self, value=Null):
        if value is Null:
            self.value = []
        else:
            self.value = list(value)

    # General Operations

    @pymethod()
    def append(self, object):
        self.value.append(object)
        return self

    @pymethod()
    def count(self, value):
        return self["Lobby"]["Number"].clone(self.value.count(value))

    @pymethod()
    def len(self):
        return self["Lobby"]["Number"].clone(leN(self.value))

    @pymethod()
    def at(self, i):
        return self.value[int(i)]

    @pymethod()
    def sort(self):
        self.value.sort()
        return self

    @pymethod()
    def sorted(self):
        return self.clone(sorted(self.value))

    # Boolean Operations

    @pymethod()
    def lt(self, other):
        test = self.value < other.value
        return self["Lobby"]["True"] if test else self["Lobby"]["False"]

    @pymethod()
    def gt(self, other):
        test = self.value > other.value
        return self["Lobby"]["True"] if test else self["Lobby"]["False"]

    # Type Conversion

    @pymethod()
    def repr(self):
        values = ", ".join([repr(x) for x in self.value])
        return self["Lobby"]["String"].clone("List(%s)" % values)
