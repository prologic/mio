from decimal import Decimal

from mio import runtime
from mio.utils import pymethod, Null

from mio.object import Object


class Number(Object):

    def __init__(self, value=0):
        super(Number, self).__init__(value=Decimal(value))

        self.create_methods()
        self["parent"] = runtime.state.find("Object")

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
        return float(self.value)

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
