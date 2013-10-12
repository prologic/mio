from decimal import Decimal

from mio import runtime
from mio.object import Object
from mio.utils import pymethod, Null


class Number(Object):

    def __init__(self, value=0):
        super(Number, self).__init__(value=Decimal(value))

        self.create_methods()
        self.parent = runtime.state.find("Object")

    def __add__(self, other):
        return self.value + other.value

    def __sub__(self, other):
        return self.value - other.value

    def __mul__(self, other):
        return self.value * other.value

    def __div__(self, other):
        return self.value / other.value

    def __mod__(self, other):
        return self.value % other.value

    def __pow__(self, other):
        return self.value ** other.value

    def __int__(self):
        return int(self.value)

    def __float__(self):
        return float(self.value * Decimal(1.0))

    def __repr__(self):
        return str(self.value)

    def __str__(self):
        return str(self.value)

    def clone(self, value=Null):
        if value is not Null:
            value = Decimal(value)
        return super(Number, self).clone(value)

    # General Arithmetic

    @pymethod("+")
    def add(self, receiver, context, m, other):
        return self.clone(receiver + other.eval(context))

    @pymethod("-")
    def sub(self, receiver, context, m, other):
        return self.clone(receiver - other.eval(context))

    @pymethod("*")
    def mul(self, receiver, context, m, other):
        return self.clone(receiver * other.eval(context))

    @pymethod("/")
    def div(self, receiver, context, m, other):
        return self.clone(receiver / other.eval(context))

    @pymethod("**")
    def pow(self, receiver, context, m, other):
        return self.clone(receiver ** other.eval(context))

    @pymethod("%")
    def mod(self, receiver, context, m, other):
        return self.clone(receiver % other.eval(context))

    # Type Conversions

    @pymethod("float")
    def float(self, receiver, context, m):
        return self.clone(float(receiver))

    @pymethod("int")
    def int(self, receiver, context, m):
        return self.clone(int(receiver))

    @pymethod("repr")
    def repr(self, receiver, context, m):
        return runtime.find("String").clone(repr(receiver))

    @pymethod("str")
    def str(self, receiver, context, m):
        return runtime.find("String").clone(str(receiver))
