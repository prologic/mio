from mio.object import Object
from mio.pymethod import pymethod

class List(Object):

    @pymethod()
    def init(self, value=None):
        self.value = list(value)

    # General Operations

    @pymethod()
    def append(self, object):
        self.value.append(object)
        return self

    @pymethod()
    def count(self):
        return self["Lobby"]["Number"].clone(self.value.count())

    # Type Conversion

    @pymethod()
    def bool(self):
        return self["Lobby"]["True"] if self.value else self["Lobby"]["False"]

    @pymethod()
    def repr(self):
        return self["Lobby"]["String"].clone(repr(self.value)) 
