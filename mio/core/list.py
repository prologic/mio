from mio import runtime
from mio.utils import pymethod, Null

from mio.object import Object

from number import Number


class List(Object):

    def __init__(self, value=[]):
        super(List, self).__init__(value=value)

        self.create_methods()
        self["parent"] = runtime.state.find("Object")

    def __iter__(self):
        return iter(self.value)

    def __repr__(self):
        values = ", ".join([repr(item) for item in self.value])
        return "list(%s)" % values

    __str__ = __repr__

    def clone(self, value=Null, type=None):
        return super(List, self).clone(value, None)

    @pymethod()
    def init(self, receiver, context, m, *args):
        args = [arg.eval(context) for arg in args]
        receiver.value = list(args)

    # General Operations

    @pymethod()
    def append(self, receiver, context, m, item):
        receiver.value.append(item.eval(context))
        return receiver

    @pymethod()
    def count(self, receiver, context, m, value):
        return Number(receiver.value.count(value.eval(context)))

    @pymethod()
    def extend(self, receiver, context, m, *args):
        args = [arg.eval(context) for arg in args]
        receiver.value.extend(args)
        return receiver

    @pymethod()
    def len(self, receiver, context, m):
        return Number(len(receiver.value))

    @pymethod()
    def at(self, receiver, context, m, index):
        return receiver.value[int(index.eval(context))]

    @pymethod()
    def reverse(self, receiver, context, m):
        receiver.value.reverse()
        return receiver

    @pymethod()
    def reversed(self, receiver, context, m):
        return receiver.clone(reversed(receiver.value))

    @pymethod()
    def sort(self, receiver, context, m):
        receiver.value.sort()
        return receiver

    @pymethod()
    def sorted(self, receiver, context, m):
        return receiver.clone(sorted(receiver.value))
