from mio.object import Object
from mio.errors import TypeError
from mio.pymethod import pymethod

class Number(Object):

    def __int__(self):
        return int(self.value)

    def __float__(self):
        return float(self.value)

    def __repr__(self):
        return str(self.value)

    __str__ = __repr__

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
