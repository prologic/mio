from copy import copy
from inspect import getmembers, ismethod

from errors import SlotError
from utils import method, Null
from pymethod import pymethod, PyMethod


class Object(object):

    __slots__ = ("slots", "protos", "value",)

    def __init__(self, value=Null, proto=None):
        super(Object, self).__init__()

        self.value = value

        self.protos = (proto,) if proto is not None else ()

        self.slots = {}

        # Setup Methods
        predicate = lambda x: ismethod(x) and getattr(x, "method", False)
        for _, method in getmembers(self, predicate):
            if method.type == "python":
                self.slots[method.name] = PyMethod(method)
            else:
                self.slots[method.name] = method

    def __getitem__(self, key):
        if key in self.slots:
            return self.slots[key]

        for proto in self.protos:
            return proto[key]

        raise SlotError(key)

    def __setitem__(self, key, value):
        self.slots[key] = value

    def __repr__(self):
        if self.value is not Null:
            return repr(self.value)
        else:
            slots = {}
            for k, v in self.slots.items():
                if isinstance(v, Object):
                    name = v.__class__.__name__
                    slots[k] = "%s_%s" % (name, id(v))
                elif isinstance(v, PyMethod):
                    slots[k] = repr(v)
                elif ismethod(v):
                    name = getattr(v, "name", "__name__")
                    slots[k] = "%s(...)" % name
                else:
                    print("Unknown Type:")
                    print(k, type(v))
            slots = "\n".join(["  %s = %s" % (str(k).ljust(15), v)
                for k, v in slots.items()])
            name = self.__class__.__name__
            return "%s_%s:\n%s" % (name, id(self), slots)

    def __str__(self):
        if self.value is not Null:
            return str(self.value)
        else:
            return ""

    def __call__(self, *args, **kwargs):
        return self

    @method()
    def method(self, receiver, context, *args):
        from method import Method
        arguments, message = args[:-1], args[-1:][0]
        return Method(context, arguments, message)

    @pymethod("print")
    def _print(self):
        print(self)
        return self

    @pymethod("slots")
    def _slots(self):
        from bootstrap import Lobby
        return Lobby["List"].clone(self.slots.keys())

    @pymethod("protos")
    def _protos(self):
        from bootstrap import Lobby
        return Lobby["List"].clone(self.protos)

    @pymethod()
    def clone(self, value=Null):
        obj = copy(self)
        obj.protos = (self,)

        if value is not Null:
            obj.value = value

        obj.slots = {}

        if hasattr(obj, "init"):
            obj.init(value)

        return obj

    @pymethod()
    def set_slot(self, name, value):
        self[name.value] = value
        return value
