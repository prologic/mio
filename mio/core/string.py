from mio import runtime
from mio.utils import method

from mio.object import Object


class String(Object):

    def __init__(self, value=""):
        super(String, self).__init__(value=value)

        self.create_methods()
        self["parent"] = runtime.state.find("Object")

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

    def __str__(self):
        return str(self.value)

    # General Operations

    @method("+")
    def add(self, receiver, context, m, other):
        return self.clone(self + str(other))

    @method("*")
    def mul(self, receiver, context, m, other):
        return self.clone(self * int(other))

    @method()
    def index(self, receiver, context, m, sub, start=None, end=None):
        return Number(self.index(sub, start, end))

    @method()
    def lower(self, receiver, context, m):
        return self.clone(self.value.lower())

    @method()
    def upper(self, receiver, context, m):
        return self.clone(self.value.upper())
