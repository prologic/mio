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
    def count(self):
        return self["Lobby"]["Number"].clone(self.value.count())

    # Boolean Operations

    @pymethod()
    def lt(self, other):
        return self["Lobby"]["Boolean"].clone(bool(self.value < other.value))

    @pymethod()
    def gt(self, other):
        return self["Lobby"]["Boolean"].clone(bool(self.value > other.value))

    @pymethod()
    def eq(self, other):
        return self["Lobby"]["Boolean"].clone(bool(self.value == other.value))

    # Type Conversion

    @pymethod()
    def bool(self):
        return self["Lobby"]["True"] if self.value else self["Lobby"]["False"]

    @pymethod()
    def repr(self):
        return self["Lobby"]["String"].clone(repr(self.value))
