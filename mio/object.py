from copy import copy
from inspect import getmembers, ismethod

from utils import Null
from errors import SlotError
from pymethod import pymethod, PyMethod

class Object(object):

    __slots__ = ("slots", "protos", "value",)

    def __init__(self, value=Null, proto=None):
        super(Object, self).__init__()

        self.value = value

        self.protos = (proto,) if proto is not None else ()

        self.slots = {}

        # Setup method
        predicate = lambda x: ismethod(x) and not x.__name__.startswith("_")
        for name, method in getmembers(self, predicate):
            self.slots[name] = method

        # Setup Python Methods
        predicate = lambda x: getattr(x, "pymethod", False)
        for name, pymethod in getmembers(self, predicate):
            self.slots[pymethod.name] = PyMethod(name)

    def __getitem__(self, key):
        if key in self.slots:
            return self.slots[key]

        message = None

        for proto in self.protos:
            message = proto[key]

        if message:
            return message
        else:
            raise SlotError(key)

    def __setitem__(self, key, value):
        self.slots[key] = value

    def __repr__(self):
        if self.value is not Null:
            return repr(self.value)
        else:
            slots = "\n".join(self.slots.keys())
            #slots = "\n".join(["  %s = %s" % (str(k).ljust(15), v)
            #    for k, v in self.slots.items() if not v is self])
            return "Object_%s:\n%s" % (id(self), slots)

    def __call__(self, *args, **kwargs):
        return self

    @pymethod("print")
    def _print(self):
        print(self)
        return self

    @pymethod("slots")
    def _slots(self):
        from bootstrap import Lobby
        return Lobby["List"].clone(self.slots.keys())

    @pymethod()
    def clone(self, value=Null):
        obj = copy(self)
        obj.protos = (self,)

        if value is not Null:
            obj.value = value

        obj.slots = {}

        return obj

    def method(self, receiver, context, *args):
        from method import Method
        arguments, message = args[:-1], args[-1:][0]
        return Method(context, arguments, message)

    @pymethod()
    def set_slot(self, name, value):
        self[name.value] = value
        return value
