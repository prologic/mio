from mio import runtime
from mio.utils import method
from mio.object import Object


class Bytes(Object):

    def __init__(self, value=b""):
        super(Bytes, self).__init__(value=value)

        self.create_methods()
        self.parent = runtime.find("Object")

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
        return self.value.decode("utf-8")

    @method()
    def init(self, receiver, context, m, value=None):
        receiver.value = value or ""

    # General Operations

    @method("+")
    def add(self, receiver, context, m, other):
        return self.clone(receiver + bytes(other.eval(context)))

    @method("*")
    def mul(self, receiver, context, m, other):
        return self.clone(receiver * int(other.eval(context)))

    @method()
    def find(self, receiver, context, m, sub, start=None, end=None):
        sub = bytes(sub.eval(context))
        start = int(start.eval(context)) if start is not None else None
        end = int(end.eval(context)) if end is not None else None
        return runtime.find("Number").clone(receiver.value.find(sub, start, end))

    @method()
    def join(self, receiver, context, m, xs):
        xs = xs.eval(context)
        return receiver.clone(receiver.value.join([bytes(x) for x in xs]))

    @method()
    def lower(self, receiver, context, m):
        return self.clone(receiver.value.lower())

    @method()
    def upper(self, receiver, context, m):
        return self.clone(receiver.value.upper())
