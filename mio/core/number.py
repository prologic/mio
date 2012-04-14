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

    # Type Conversion

    @pymethod()
    def str(self):
        return self["Lobby"]["String"].clone(str(self.value)) 

    @pymethod()
    def int(self):
        return self.clone(nt(self.value))

    @pymethod()
    def float(self):
        return self.clone(float(self.value))
