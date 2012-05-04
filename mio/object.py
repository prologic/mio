import sys
from copy import copy
from inspect import  getmembers, ismethod

from errors import KeyError
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
        keys = self.__class__.__dict__.keys()
        parent = self.attrs.get("parent", {})
        predicate = lambda x: ismethod(x) and getattr(x, "method", False)
        in_self = lambda k: k in keys
        in_parent = lambda k: k in parent
        for _, method in getmembers(self, predicate):
            if not in_self(method.name) and in_parent(method.name):
                continue

            if method.type == "python":
                self[method.name] = PyMethod(method)
            else:
                self[method.name] = method

        keys = dir(self)
        for k, v in self.attrs.items():
            if k not in keys and k in self.attrs.get("parent", {}):
                del self.attrs[k]


    def __hash__(self):
        return hash(self.value)
    
    def __eq__(self, other):
        return self.value == other.value

    def __cmp__(self, other):
        return cmp(self.value, other.value)

    def __contains__(self, key):
        return key in self.attrs

    def __delitem__(self, key):
        if key in self.attrs:
            del self.attrs[key]

    def __getitem__(self, key):
        if key in self.attrs:
            return self.attrs[key]

        parent = self.attrs.get("parent")
        while parent is not None:
            if key in parent:
                return parent[key]
            parent = parent.attrs.get("parent")

        if hasattr(self, "forward"):
            return self.forward(key)
        else:
            raise KeyError(self, key)

    def __setitem__(self, key, value):
        self.attrs[key] = value

    def __call__(self, *args, **kwargs):
        return self

    def __repr__(self):
        type = self.attrs.get("type", self.__class__.__name__)
        default = "%s_%s" % (type, hex(id(self)))
        return repr(self.value) if self.value is not Null else default

    def __str__(self):
        return str(self.value) if self.value is not Null else ""

    # Attribute Operations

    @method("del")
    def _del(self, receiver, context, m, key):
        key = key(context).value if key.type else key.name
        return receiver.get(key, self["None"])

    @method()
    def has(self, receiver, context, m, key):
        key = key(context).value if key.type else key.name
        test = key in receiver
        return self["True"] if test else self["False"]

    @method()
    def set(self, receiver, context, m, key, value):
        key = key(context).value if key.type else key.name
        receiver[key] = value(context)
        return receiver[key]

    @method()
    def get(self, receiver, context, m, key, default=None):
        key = key(context).value if key.type else key.name
        return receiver.attrs.get(key, default)

    @pymethod()
    def forward(self, key):
        if key in self["Lobby"]:
            return self["Lobby"][key]
        else:
            raise KeyError(self, key)

    # Argument Operations

    @method()
    def arg(self, receiver, context, m, at, default=None):
        try:
            index = int(at(context))
            caller = context["caller"]
            args = context["args"].value
            if index is not None and index < len(args):
                return args[index](caller)
            else:
                return self.get("None", default)(caller)
        except SlotError:
            return at(context)

    # Method Operations

    @method("method")
    def _method(self, receiver, context, m, *args):
        from method import Method
        arguments, message = args[:-1], args[-1:][0]
        return Method(context, arguments, message, parent=self["Object"])

    # Flow Control

    @method()
    def foreach(self, receiver, context, m, *args):
        result = self["None"]
        self["state"].reset()

        vars, expression = args[:-1], args[-1]

        for item in receiver:
            if len(vars) == 2:
                context[vars[0].name], context[vars[1].name] = item
            elif len(vars) == 1:
                context[vars[0].name] = item

            result = expression(context)

        self["state"].reset()
        return result

    @method("while")
    def _while(self, receiver, context, m, condition, expression):
        result = self["None"]

        self["state"].reset()

        while condition(context).value and (not self["state"].stop()):
            result = expression(context)

        self["state"].reset()

        return result

    @method("if")
    def _if(self, reciver, context, *args):
        test = bool(args[0](context).value)
        index = 1 if test else 2
        if index < len(args):
            return args[index](context)

        return self["True"] if test else self["False"]

    # I/O

    @pymethod("print")
    def _print(self):
        sys.stdout.write("%s" % self.value)
        return self

    @pymethod()
    def println(self):
        sys.stdout.write("%s\n" % self.value)
        return self

    @pymethod()
    def write(self, *args):
        sys.stdout.write("%s" % " ".join([str(arg) for arg in args]))
        return self["None"]

    @pymethod()
    def writeln(self, *args):
        sys.stdout.write("%s\n" % " ".join([str(arg) for arg in args]))
        return self["None"]

    # Introspection

    @pymethod()
    def type(self):
        default = self.__class__.__name__
        return self["String"].clone(self.attrs.get("type", default))

    @pymethod()
    def hash(self):
        return self["Number"].clone(hash(self))

    @pymethod()
    def id(self):
        return self["Number"].clone(id(self))

    @pymethod()
    def keys(self):
        return self["List"].clone(self.attrs.keys())

    @pymethod()
    def summary(self):
        sys.stdout.write("%s\n" % format_object(self))
        return self

    # Object Operations

    @method()
    def do(self, receiver, context, m, expression):
        return expression(receiver)

    def clone(self, value=Null, type=Null):
        obj = copy(self)

        obj.attrs = {}
        obj["parent"] = self

        if value is not Null:
            obj.value = value

        if type is not Null:
            obj["type"] = type

        return obj

    @method("clone")
    def _clone(self, receiver, context, m, *args):
        type = self["String"].clone(m.parent.args[0].name)
        cloned = self.clone(type=type)
        if "init" in cloned:
            cloned["init"](context, *args)
        return cloned

    # Boolean Operations

    @pymethod()
    def eq(self, other):
        test = self == other
        return self["True"] if test else self["False"]

    @pymethod()
    def cmp(self, other):
        return self["Number"].clone(cmp(self, other))

    @pymethod("and")
    def _and(self, other):
        return self.clone(self and other)

    @pymethod("or")
    def _or(self, other):
        return self.clone(self or other)

    @pymethod("not")
    def _not(self, value=Null):
        if not value is Null:
            return value.clone(not value)
        else:
            return self.clone(not self)

    # Type Conversion

    @pymethod()
    def repr(self):
        return self["String"].clone(repr(self))

    @pymethod("str")
    def str(self):
        return self["String"].clone(str(self))
