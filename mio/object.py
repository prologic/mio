from copy import copy
from inspect import  getmembers, isfunction, ismethod

from errors import SlotError
from pymethod import pymethod, PyMethod
from utils import format_method, method, Null


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

    def __contains__(self, key):
        return key in self.slots

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
                elif ismethod(v) or isfunction(v):
                    slots[k] = format_method(v)
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

    # Slot Operations

    @method()
    def set_slot(self, receiver, context, key, value):
        key = key(context).value if key.type else key.name
        receiver[key] = value(context)
        return receiver[key]

    # Argument Operations

    @method()
    def eval_arg(self, receiver, context, at, default=None):
        from bootstrap import Lobby
        try:
            index = at(context).value
            caller = context["caller"]
            args = context["args"].value
            if index is not None and index < len(args):
                return args[index](caller)
            else:
                if default is not None:
                    return default(caller)
                else:
                    return Lobby["None"](caller)
        except SlotError:
            return at(context)

    # Method Operations

    @method("method")
    def _method(self, receiver, context, *args):
        from method import Method
        from bootstrap import Lobby
        arguments, message = args[:-1], args[-1:][0]
        return Method(context, arguments, message, proto=Lobby["Object"])

    # Flow Control

    @method("if")
    def _if(self, reciver, context, *args):
        condition = args[0](context).value == True
        index = 1 if condition else 2
        if index < len(args):
            return args[index](context)

        from bootstrap import Lobby
        return Lobby["Boolean"].clone(condition)

    # I/O

    @pymethod("print")
    def _print(self):
        print(self)
        return self

    # Introspection

    @pymethod("slots")
    def _slots(self):
        from bootstrap import Lobby
        return Lobby["List"].clone(self.slots.keys())

    @pymethod("protos")
    def _protos(self):
        from bootstrap import Lobby
        return Lobby["List"].clone(self.protos)

    # Object Operations

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

    # Boolean Operations

    @pymethod("and")
    def _and(self, other):
        return self.clone(self.value and other.value)

    @pymethod("or")
    def _or(self, other):
        return self.clone(self.value or other.value)

    @pymethod("not")
    def _not(self, other):
        return self.clone(not self.value)
