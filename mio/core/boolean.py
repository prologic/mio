from mio.object import Object
from mio.pymethod import pymethod


class Boolean(Object):

    # General Boolean Logic

    @pymethod("and")
    def _and(self, other):
        return self.clone(self.value and other.value)

    @pymethod("or")
    def _or(self, other):
        return self.clone(self.value or other.value)

    @pymethod("not")
    def _not(self, other):
        return self.clone(not self.value)

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
