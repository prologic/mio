from mio.object import Object
from mio.pymethod import pymethod


class String(Object):

    # General Operations

    @pymethod()
    def add(self, other):
        return self.clone(self.value + other.value)

    @pymethod()
    def index(self, sub, start=None, end=None):
        return self["Lobby"]["Number"].clone(self.index(sub, start, end))

    @pymethod()
    def lower(self):
        return self.clone(self.value.lower())

    @pymethod()
    def upper(self):
        return self.clone(self.value.upper())

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
        return self["Lobby"]["Boolean"].clone(self.value)

    @pymethod()
    def int(self):
        return self["Lobby"]["Boolean"].clone(int(self.value))

    @pymethod()
    def float(self):
        return self["Lobby"]["Boolean"].clone(float(self.value))

    @pymethod()
    def repr(self):
        return self["Lobby"]["String"].clone(repr(self.value)) 

    @pymethod()
    def str(self):
        return self["Lobby"]["String"].clone(str(self.value)) 
