from mio.object import Object
from mio.pymethod import pymethod


class Boolean(Object):

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
        return self["Lobby"]["Boolean"].clone(bool(self.value))

    @pymethod()
    def int(self):
        return self["Lobby"]["Number"].clone(int(self.value))

    @pymethod()
    def float(self):
        return self["Lobby"]["Number"].clone(float(self.value))

    @pymethod()
    def repr(self):
        return self["Lobby"]["String"].clone(repr(self.value))

    @pymethod()
    def str(self):
        return self["Lobby"]["String"].clone(str(self.value))
