from mio import runtime
from mio.errors import TypeError
from mio.utils import method, Null

from mio.object import Object

from number import Number


class List(Object):

    def __init__(self, value=[]):
        super(List, self).__init__(value=value)

        self.create_methods()
        self.parent = runtime.state.find("Object")

    def __iter__(self):
        return iter(self.value)

    def __repr__(self):
        values = ", ".join([repr(item) for item in self.value])
        return "list(%s)" % values

    __str__ = __repr__

    @method()
    def init(self, receiver, context, m, iterable=None):
        if iterable is not None:
            iterable = iterable.eval(context)
        else:
            iterable = runtime.find("List").clone()

        receiver.value = list(iterable)

    # General Operations

    @method()
    def append(self, receiver, context, m, item):
        receiver.value.append(item.eval(context))
        return receiver

    @method()
    def count(self, receiver, context, m, value):
        return Number(receiver.value.count(value.eval(context)))

    @method()
    def extend(self, receiver, context, m, *args):
        args = [arg.eval(context) for arg in args]
        receiver.value.extend(args)
        return receiver

    @method()
    def len(self, receiver, context, m):
        return Number(len(receiver.value))

    @method()
    def at(self, receiver, context, m, index):
        return receiver.value[int(index.eval(context))]

    @method()
    def reverse(self, receiver, context, m):
        receiver.value.reverse()
        return receiver

    @method()
    def reversed(self, receiver, context, m):
        return receiver.clone(list(reversed(receiver.value)))

    @method()
    def sort(self, receiver, context, m):
        receiver.value.sort()
        return receiver

    @method()
    def sorted(self, receiver, context, m):
        return receiver.clone(list(sorted(receiver.value)))
