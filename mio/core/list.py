from mio import runtime
from mio.utils import method

from mio.object import Object

from number import Number


class List(Object):

    def __init__(self, value=[]):
        super(List, self).__init__(value=value)

        self.create_methods()
        self["parent"] = runtime.state.find("Object")

    def __iter__(self):
        return iter(self.value)

    def __str__(self):
        return "[%s]" % ", ".join([repr(x) for x in self.value])

    @method()
    def init(self, receiver, context, m, *args):
        self.value = list(args)

    # General Operations

    @method()
    def append(self, receiver, context, m, item):
        receiver.value.append(item(context))
        return receiver

    @method()
    def count(self, receiver, context, m, value):
        return Number(receiver.value.count(value(context)))

    @method()
    def extend(self, receiver, context, m, *args):
        args = [arg(context) for arg in args]
        receiver.value.extend(args)
        return receiver

    @method()
    def len(self):
        return Number(len(receiver.value))

    @method()
    def at(self, receiver, context, m, index):
        return receiver.value[int(index(context))]

    @method()
    def reverse(self, receiver, context, m):
        receiver.value.reverse()
        return receiver

    @method()
    def reversed(self, receiver, context, m):
        return self.clone(reversed(receiver.value))

    @method()
    def sort(self, receiver, context, m):
        receiver.value.sort()
        return receiver

    @method()
    def sorted(self, receiver, context, m):
        return self.clone(sorted(receiver.value))
