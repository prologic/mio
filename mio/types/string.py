from mio import runtime
from mio.utils import method

from mio.object import Object

from number import Number


class String(Object):

    def __init__(self, value=""):
        super(String, self).__init__(value=value)

        self.create_methods()
        self.parent = runtime.state.find("Object")

    def __iter__(self):
        for c in self.value:
            yield self.clone(c)

    def __add__(self, other):
        return self.value + other

    def __mul__(self, other):
        return self.value * other

    def __int__(self):
        return int(self.value)

    def __float__(self):
        return float(self.value)

    def __repr__(self):
        return repr(self.value)

    def __str__(self):
        return str(self.value)

    @method()
    def init(self, receiver, context, m, value=None):
        receiver.value = value.eval(context) if value is not None else ""

    # General Operations

    @method("+")
    def add(self, receiver, context, m, other):
        return self.clone(receiver + str(other.eval(context)))

    @method("*")
    def mul(self, receiver, context, m, other):
        return self.clone(receiver * int(other.eval(context)))

    @method()
    def find(self, receiver, context, m, sub, start=None, end=None):
        sub = str(sub.eval(context))
        start = int(start.eval(context)) if start is not None else None
        end = int(end.eval(context)) if end is not None else None
        return Number(receiver.value.find(sub, start, end))

    @method()
    def lower(self, receiver, context, m):
        return self.clone(receiver.value.lower())

    @method()
    def upper(self, receiver, context, m):
        return self.clone(receiver.value.upper())
