from mio.object import Object
from mio.pymethod import pymethod


class String(Object):

    def __iter__(self):
        for c in self.value:
            yield self.clone(c)

    def __int__(self):
        return int(self.value)

    def __float__(self):
        return float(self.value)

    def __str__(self):
        return str(self.value)

    # General Operations

    @pymethod()
    def add(self, other):
        return self.clone(self.value + other.value)

    @pymethod()
    def index(self, sub, start=None, end=None):
        return self["Lobby"]["Number"].clone(self.index(sub, start, end))

    @pymethod()
    def lower(self):
        return self.clone(self.value.lower())

    @pymethod()
    def upper(self):
        return self.clone(self.value.upper())
