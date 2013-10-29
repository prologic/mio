from decimal import Decimal


from mio import runtime
from mio.object import Object
from mio.utils import method, Null


class Number(Object):

    def __init__(self, value=0):
        super(Number, self).__init__(value=Decimal(value))

        self.create_methods()
        self.parent = runtime.find("Object")

    def __abs__(self):
        return abs(self.value)

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

    # Type Conversions

    @method("float")
    def float(self, receiver, context, m):
        return self.clone(float(receiver))

    @method("int")
    def int(self, receiver, context, m):
        return self.clone(int(receiver))
