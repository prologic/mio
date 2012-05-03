from mio.object import Object
from mio.errors import TypeError
from mio.pymethod import pymethod

class Number(Object):

    def __add__(self, other):
        return self.value.__add__(other.value)

    def __sub__(self, other):
        return self.value.__sub__(other.value)

    def __mul__(self, other):
        return self.value.__mul__(other.value)

    def __div__(self, other):
        return self.value.__div__(other.value)

    def __mod__(self, other):
        return self.value.__mod__(other.value)

    def __pow__(self, other):
        return self.value.__pow__(other.value)

    def __int__(self):
        return self.value.__int__()

    def __float__(self):
        return self.value.__float__()

    def __repr__(self):
        return str(self.value)

    __str__ = __repr__

    # General Arithmetic

    @pymethod()
    def add(self, other):
        return self.clone(self + other)

    @pymethod()
    def sub(self, other):
        return self.clone(self - other)

    @pymethod()
    def mul(self, other):
        return self.clone(self * other)

    @pymethod()
    def div(self, other):
        return self.clone(self / other)

    @pymethod()
    def pow(self, other):
        return self.clone(self ** other)

    @pymethod()
    def mod(self, other):
        return self.clone(self % other)

    @pymethod()
    def lshift(self, other):
        return self.clone(self * 2 ** other)

    @pymethod()
    def rshift(self, other):
        return self.clone(self/ 2 ** other)
