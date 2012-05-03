from mio.utils import Null
from mio.object import Object
from mio.pymethod import pymethod


class List(Object):

    def __iter__(self):
        for i in self.value:
            yield i

    def __repr__(self):
        return "[%s]" % ", ".join([repr(x) for x in self.value])

    __str__ = __repr__

    @pymethod()
    def init(self, value=Null):
        if value is Null:
            self.value = []
        else:
            self.value = list(value)

    # General Operations

    @pymethod()
    def append(self, object):
        self.value.append(object)
        return self

    @pymethod()
    def count(self, value):
        return self["Lobby"]["Number"].clone(self.value.count(value))

    @pymethod()
    def extend(self, *args):
        self.value.extend(args)
        return self

    @pymethod()
    def len(self):
        return self["Lobby"]["Number"].clone(len(self.value))

    @pymethod()
    def at(self, i):
        return self.value[int(i)]

    @pymethod()
    def reverse(self):
        self.value.reverse()
        return self

    @pymethod()
    def reversed(self):
        return self.clone(reversed(self.value))

    @pymethod()
    def sort(self):
        self.value.sort()
        return self

    @pymethod()
    def sorted(self):
        return self.clone(sorted(self.value))
