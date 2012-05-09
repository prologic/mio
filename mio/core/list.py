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
    def append(self, receiver, context, m, object):
        self.value.append(object)
        return self

    @method()
    def count(self, receiver, context, m, value):
        return Number(self.value.count(value))

    @method()
    def extend(self, receiver, context, m, *args):
        self.value.extend(list(args))
        return self

    @method()
    def len(self):
        return Number(len(self.value))

    @method()
    def at(self, receiver, context, m, index):
        return self.value[int(index)]

    @method()
    def reverse(self, receiver, context, m):
        self.value.reverse()
        return self

    @method()
    def reversed(self, receiver, context, m):
        return self.clone(reversed(self.value))

    @method()
    def sort(self, receiver, context, m):
        self.value.sort()
        return self

    @method()
    def sorted(self, receiver, context, m):
        return self.clone(sorted(self.value))
