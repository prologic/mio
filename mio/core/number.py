from mio.object import Object
from mio.errors import TypeError
from mio.pymethod import pymethod

class Number(Object):

    def __int__(self):
        return int(self.value)

    def __str__(self):
        return str(self.value)

    __repr__ = __str__

    # General Arithmetic

    @pymethod()
    def add(self, other):
        if type(self.value) is not type(other.value):
            raise TypeError(self.add, self._type(), other._type())
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

    @pymethod()
    def pow(self, other):
        return self.clone(self.value ** other.value)

    @pymethod()
    def mod(self, other):
        return self.clone(self.value % other.value)

    @pymethod()
    def lshift(self, other):
        return self.clone(self.value * 2 ** other.value)

    @pymethod()
    def rshift(self, other):
        return self.clone(self.value / 2 ** other.value)

    # Boolean Operations

    @pymethod()
    def cmp(self, other):
        if type(self.value) is not type(other.value):
            raise TypeError(self.cmp, self._type(), other._type())
        return self.clone(self.value.compare(other.value))
        

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
    def int(self):
        return self.clone(nt(self.value))

    @pymethod()
    def float(self):
        return self.clone(float(self.value))

    @pymethod()
    def str(self):
        return self["Lobby"]["String"].clone(str(self.value)) 

    repr = str
