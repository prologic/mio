from copy import copy
from inspect import  getmembers, isfunction, ismethod

from errors import SlotError
from utils import format_method, method, Null
from pymethod import pymethod, PyMethod


class Object(object):

    __slots__ = ("attrs", "value",)

    def __init__(self, value=Null, parent=None):
        super(Object, self).__init__()

        self.attrs = {}
        self.value = value

        self["parent"] = parent if parent is not None else self

        # Setup Methods
        predicate = lambda x: ismethod(x) and getattr(x, "method", False)
        for _, method in getmembers(self, predicate):
            if method.type == "python":
                self[method.name] = PyMethod(method)
            else:
                self[method.name] = method

    def __contains__(self, key):
        return key in self.attrs

    def __getitem__(self, key):
        if key in self.attrs:
            return self.attrs[key]

        parent = self["parent"]
        while parent is not self:
            if key in parent:
                return parent[key]
            parent = parent["parent"]

        raise SlotError(key)

    def __setitem__(self, key, value):
        self.attrs[key] = value

    def __call__(self, *args, **kwargs):
        return self

    def __repr__(self):
        return repr(self.value) if self.value is not Null else self.pprint()

    def __str__(self):
        return str(self.value) if self.value is not Null else ""

    def keys(self):
        return self.attrs.keys()

    def pprint(self):
        attrs = {}
        for k, v in self.attrs.items():
            if isinstance(v, Object):
                name = v.__class__.__name__
                attrs[k] = "%s_%s" % (name, id(v))
            elif isinstance(v, PyMethod):
                attrs[k] = repr(v)
            elif ismethod(v) or isfunction(v):
                attrs[k] = format_method(v)
            else:
                print("Unknown Type:")
                print(k, type(v))
        attrs = "\n".join(["  %s = %s" % (str(k).ljust(15), v)
            for k, v in sorted(attrs.items())])
        name = self.__class__.__name__
        return "%s_%s:\n%s" % (name, id(self), attrs)

    @property
    def parent(self):
        return self["parent"]

    @parent.setter
    def parent(self, parent):
        self["parent"] = parent

    # Slot Operations

    @method("del")
    def _del(self, receiver, context, key):
        key = key(context).value if key.type else key.name
        return receiver.get(key, self["Lobby"]["None"])

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
        return receiver.attrs.get(key, default)

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
        test = args[0](context).value == True
        index = 1 if test else 2
        if index < len(args):
            return args[index](context)

        return self["Lobby"]["True"] if test else self["Lobby"]["False"]

    # I/O

    @pymethod("print")
    def _print(self):
        print(self.value)
        return self

    @pymethod("println")
    def _println(self):
        print("%s\n" % self.value)
        return self

    @pymethod("write")
    def _write(self, *args):
        print(" ".join([str(arg) for arg in args]))
        return self["Lobby"]["None"]

    @pymethod("writeln")
    def _writeln(self, *args):
        print("%s\n" % " ".join([str(arg) for arg in args]))
        return self["Lobby"]["None"]

    # Introspection

    @pymethod("type")
    def _type(self):
        from bootstrap import Lobby
        return Lobby["String"].clone(self.__class__.__name__)

    @pymethod("id")
    def _id(self):
        from bootstrap import Lobby
        return Lobby["Number"].clone(id(self))

    @pymethod("keys")
    def _keys(self):
        from bootstrap import Lobby
        return Lobby["List"].clone(self.keys())

    # Object Operations

    @method()
    def do(self, receiver, context, message):
        return message(receiver)

    @pymethod()
    def clone(self, value=Null):
        obj = copy(self)

        if value is not Null:
            obj.value = value

        obj.attrs = {}
        obj["parent"] = self

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
    def _not(self):
        return self.clone(not self.value)

    # Type Conversion

    @pymethod("bool")
    def bool(self):
        test = bool(self.value)
        return self["Lobby"]["True"] if test else self["Lobby"]["False"]

    @pymethod()
    def repr(self):
        from bootstrap import Lobby
        return Lobby["String"].clone(repr(self))

    @pymethod("str")
    def str(self):
        from bootstrap import Lobby
        return Lobby["String"].clone(str(self))
