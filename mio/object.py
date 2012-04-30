from copy import copy
from inspect import  getmembers, ismethod

from errors import SlotError
from pymethod import pymethod, PyMethod
from utils import format_object, method, Null


class Object(object):

    __slots__ = ("attrs", "value",)

    def __init__(self, value=Null, parent=None):
        super(Object, self).__init__()

        self.attrs = {}
        self.value = value

        if parent is not None:
            self["parent"] = parent

        # Setup Methods
        predicate = lambda x: ismethod(x) and getattr(x, "method", False)
        for _, method in getmembers(self, predicate):
            if method.name in self.attrs.get("parent", ()):
                continue

            if method.type == "python":
                self[method.name] = PyMethod(method)
            else:
                self[method.name] = method

    def __contains__(self, key):
        return key in self.attrs

    def __getitem__(self, key):
        if key in self.attrs:
            return self.attrs[key]

        parent = self.attrs.get("parent")
        while parent is not None:
            if key in parent:
                return parent[key]
            parent = parent.attrs.get("parent")

        raise SlotError(key)

    def __setitem__(self, key, value):
        self.attrs[key] = value

    def __call__(self, *args, **kwargs):
        return self

    def __repr__(self):
        default = "%s_%s" % (self.__class__.__name__, hex(id(self)))
        return repr(self.value) if self.value is not Null else default

    def __str__(self):
        return str(self.value) if self.value is not Null else ""

    def lobby(self, key, default=None):
        return self["Lobby"].attrs.get(key, default)

    # Slot Operations

    @method("del")
    def _del(self, receiver, context, key):
        key = key(context).value if key.type else key.name
        return receiver.get(key, self.lobby("None"))

    @method()
    def has(self, receiver, context, key):
        key = key(context).value if key.type else key.name
        test = key in receiver
        lobby = self.lobby
        return lobby("True") if test else lobby("False")

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
        try:
            index = int(at(context))
            caller = context["caller"]
            args = context["args"].value
            if index is not None and index < len(args):
                return args[index](caller)
            else:
                return self.lobby("None", default)(caller)
        except SlotError:
            return at(context)

    # Method Operations

    @method("method")
    def _method(self, receiver, context, *args):
        from method import Method
        arguments, message = args[:-1], args[-1:][0]
        return Method(context, arguments, message, parent=self.lobby("Object"))

    # Flow Control

    @method("if")
    def _if(self, reciver, context, *args):
        test = args[0](context).value == True
        index = 1 if test else 2
        if index < len(args):
            return args[index](context)

        lobby = self.lobby
        return lobby("True") if test else lobby("False")

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
        return self.lobby("None")

    @pymethod("writeln")
    def _writeln(self, *args):
        print("%s\n" % " ".join([str(arg) for arg in args]))
        return self.lobby("None")

    # Introspection

    @pymethod("type")
    def _type(self):
        return self.lobby("String").clone(self.__class__.__name__)

    @pymethod("id")
    def _id(self):
        return self.lobby("Number").clone(id(self))

    @pymethod("keys")
    def _keys(self):
        return self.lobby("List").clone(self.attrs.keys())

    @pymethod()
    def summary(self):
        print format_object(self)
        return self

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
        lobby = self.lobby
        return lobby("True") if test else lobby("False")

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
        lobby = self.lobby
        return lobby("True") if test else lobby("False")

    @pymethod()
    def repr(self):
        return self.lobby("String").clone(repr(self))

    @pymethod("str")
    def str(self):
        return self.lobby("String").clone(str(self))
