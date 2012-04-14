from mio.object import Object
from mio.pymethod import pymethod

class Number(Object):

    # General Arithmetic

    @pymethod()
    def __add__(self, other):
        return self.clone(self.value.__add__(other.value))

    @pymethod()
    def __sub__(self, other):
        return self.clone(self.value.__sub__(other.value))

    @pymethod()
    def __mul__(self, other):
        return self.clone(self.value.__mul__(other.value))

    @pymethod()
    def __div__(self, other):
        return self.clone(self.value.__div__(other.value))

    # Type Conversion

    @pymethod()
    def __str__(self):
        return self["Lobby"]["String"].clone(str(self.value)) 

    @pymethod()
    def __int__(self):
        return self.clone(self.value.__int__())

    @pymethod()
    def __float__(self):
        return self.clone(self.value.__float__())
