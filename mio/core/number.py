from mio.object import Object
from mio.pymethod import pymethod

class Number(Object):

    # General Arithmetic

    @pymethod()
    def add(self, other):
        return self.clone(self.value + other.value)

    @pymethod()
    def sub(self, other):
        return self.clone(self.value - other.value)

    @pymethod()
    def mul(self, other):
        return self.clone(self.value * other.value)

    @pymethod()
    def div(self, other):
        return self.clone(self.value / other.value)

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
    def int(self):
        return self.clone(nt(self.value))

    @pymethod()
    def float(self):
        return self.clone(float(self.value))

    @pymethod()
    def repr(self):
        return self["Lobby"]["String"].clone(repr(self.value)) 

    @pymethod()
    def str(self):
        return self["Lobby"]["String"].clone(str(self.value)) 
