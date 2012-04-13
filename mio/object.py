from copy import copy
from inspect import getmembers
from functools import update_wrapper

from utils import Null
from errors import SlotError


class Method(object):

    def __init__(self, method):
        super(Method, self).__init__()

        self.method = method

    def __call__(self, receiver, context, *args):
        args = [arg(context) for arg in args]
        return getattr(receiver, self.method)(*args)

    def __repr__(self):
        return "%s(...)" % self.method

def method(name=None):
    def wrapper(f):
        f.name = name or f.__name__
        f.method = True
        return f

    return wrapper


class Object(object):

    __slots__ = ("slots", "protos", "value",)

    def __init__(self, value=Null, proto=None):
        super(Object, self).__init__()

        self.value = value

        self.protos = (proto,) if proto is not None else ()

        self.slots = {}

        predicate = lambda x: getattr(x, "method", False)
        for name, method in getmembers(self, predicate):
            self.slots[method.name] = Method(name)

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
            slots = "\n".join(["  %s = %s" % (str(k).ljust(15), v)
                for k, v in self.slots.items() if not v is self])
            return "Object_%s:\n%s" % (id(self), slots)

    def __call__(self, *args, **kwargs):
        return self

    @method("print")
    def _print(self):
        print(self)
        return self

    @method("slots")
    def _slots(self):
        return Lobby["List"].clone(receiver.slots.keys())

    @method()
    def clone(self, value=Null):
        obj = copy(self)
        obj.protos = (self,)

        if value is not Null:
            obj.value = value

        obj.slots = {}

        return obj

    @method()
    def set_slot(self, name, value):
        self[name.value] = value
        return value
