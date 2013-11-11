from mio import runtime
from mio.utils import method
from mio.object import Object
from mio.lexer import encoding
from mio.core.message import Message
from mio.errors import AttributeError


class String(Object):

    def __init__(self, value=u""):
        super(String, self).__init__(value=value)

        self.create_methods()
        try:
            self.parent = runtime.find("String")
        except AttributeError:
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
        return "u\"{0:s}\"".format(self.value)

    def __bytes__(self):
        return self.value.encode(encoding)

    def __str__(self):
        return self.value

    @method()
    def init(self, receiver, context, m, value=None):
        receiver.value = value or u""
        return receiver

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
        return runtime.find("Number").clone(receiver.value.find(sub, start, end))

    @method()
    def format(self, receiver, context, m, *args):
        args = [str(arg.eval(context)) for arg in args]
        return receiver.clone(receiver.value.format(*args))

    @method()
    def join(self, receiver, context, m, *args):
        if len(args) == 1 and isinstance(args[0], Message):
            args = args[0].eval(context)
        else:
            args = [arg.eval(context) if isinstance(arg, Message) else arg for arg in args]
        return receiver.clone(receiver.value.join(map(str, args)))

    @method()
    def lower(self, receiver, context, m):
        return self.clone(receiver.value.lower())

    @method()
    def upper(self, receiver, context, m):
        return self.clone(receiver.value.upper())
