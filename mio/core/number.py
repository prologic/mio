from decimal import Decimal

from mio import runtime
from mio.utils import method

from mio.object import Object


class Number(Object):

    def __init__(self, value=Decimal(0)):
        super(Number, self).__init__(value=value)

        self.create_methods()
        self["parent"] = runtime.state.find("Object")

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

    def __str__(self):
        return str(self.value)

    # General Arithmetic

    @method("+")
    def add(self, receiver, context, m, other):
        return self.clone(receiver + other.eval(context))

    @method("-")
    def sub(self, receiver, context, m, other):
        return self.clone(receiver - other.eval(context))

    @method("*")
    def mul(self, receiver, context, m, other):
        return self.clone(receiver * other.eval(context))

    @method("/")
    def div(self, receiver, context, m, other):
        return self.clone(receiver / other.eval(context))

    @method("**")
    def pow(self, receiver, context, m, other):
        return self.clone(receiver ** other.eval(context))

    @method("%")
    def mod(self, receiver, context, m, other):
        return self.clone(receiver % other.eval(context))

    @method("<<")
    def lshift(self, receiver, context, m, other):
        return self.clone(receiver * 2 ** other.eval(context))

    @method(">>")
    def rshift(self, receiver, context, m, other):
        return self.clone(receiver / 2 ** other.eval(context))
