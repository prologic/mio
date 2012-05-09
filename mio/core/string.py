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
        return self.clone(receiver + str(other(context)))

    @method("*")
    def mul(self, receiver, context, m, other):
        return self.clone(receiver * int(other(context)))

    @method()
    def index(self, receiver, context, m, sub, start=None, end=None):
        sub = sub(context)
        start = start(context) if start else None
        end = end(context) if end else None
        return Number(receiver.index(sub, start, end))

    @method()
    def lower(self, receiver, context, m):
        return self.clone(receiver.value.lower())

    @method()
    def upper(self, receiver, context, m):
        return self.clone(receiver.value.upper())
