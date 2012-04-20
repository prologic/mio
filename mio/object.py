from copy import copy
from inspect import  getmembers, isfunction, ismethod

from errors import SlotError
from pymethod import pymethod, PyMethod
from utils import format_method, method, Null


class Object(object):

    __slots__ = ("slots", "parent", "value",)

    def __init__(self, value=Null, parent=None):
        super(Object, self).__init__()

        self.value = value
        self.parent = parent

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

        parent = self.parent
        while parent is not None:
            if key in parent:
                return parent[key]
            parent = parent.parent

        raise SlotError(key)

    def __setitem__(self, key, value):
        self.slots[key] = value

    def __call__(self, *args, **kwargs):
        return self

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

    # Slot Operations

    @method("del")
    def _del(self, receiver, context, key):
        key = key(context).value if key.type else key.name
        return receiver.slots.pop(key, self["Lobby"]["None"])

    @method()
    def has(self, receiver, context, key):
        key = key(context).value if key.type else key.name
        test = key in receiver
        return self["Lobby"]["True"] if test else self["Lobby"]["False"]

    @method()
    def set(self, receiver, context, key, value):
        key = key(context).value if key.type else key.name
        receiver[key] = value(context)
        return receiver[key]

    @method()
    def get(self, receiver, context, key, default=None):
        key = key(context).value if key.type else key.name
        return receiver.slots.get(key, default)

    # Argument Operations

    @method()
    def arg(self, receiver, context, at, default=None):
        from bootstrap import Lobby
        try:
            index = int(at(context))
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
        return Method(context, arguments, message, parent=Lobby["Object"])

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
        print(self.value)
        return self

    # Introspection

    @pymethod("type")
    def _type(self):
        from bootstrap import Lobby
        return Lobby["String"].clone(self.__class__.__name__)

    @pymethod("id")
    def _id(self):
        from bootstrap import Lobby
        return Lobby["Number"].clone(id(self))

    @pymethod("slots")
    def _slots(self):
        from bootstrap import Lobby
        return Lobby["List"].clone(self.slots.keys())

    @pymethod("parent")
    def _parent(self):
        from bootstrap import Lobby
        if self.parent is not None:
            return self.parent
        else:
            return Lobby["None"]

    # Object Operations

    @method()
    def do(self, receiver, context, message):
        return message(receiver)

    @pymethod()
    def clone(self, value=Null):
        obj = copy(self)
        obj.parent = self

        if value is not Null:
            obj.value = value

        obj.slots = {}

        if hasattr(obj, "init"):
            obj.init(value)

        return obj

    # Boolean Operations

    @pymethod("eq")
    def _eq(self, other):
        test = self.value == other.value
        return self["Lobby"]["True"] if test else self["Lobby"]["False"]

    @pymethod("and")
    def _and(self, other):
        return self.clone(self.value and other.value)

    @pymethod("or")
    def _or(self, other):
        return self.clone(self.value or other.value)

    @pymethod("not")
    def _not(self, other):
        return self.clone(not self.value)

    # Type Conversion

    @pymethod("bool")
    def bool(self):
        from bootstrap import Lobby
        return Lobby["Boolean"].clone(bool(self.value))

    @pymethod()
    def repr(self):
        from bootstrap import Lobby
        return Lobby["String"].clone(repr(self))

    @pymethod("str")
    def str(self):
        from bootstrap import Lobby
        return Lobby["String"].clone(str(self))
