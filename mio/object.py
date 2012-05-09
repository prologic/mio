import sys
from copy import copy
from inspect import  getmembers, ismethod

import runtime
from errors import KeyError
from utils import format_object, method


class Object(object):

    __slots__ = ("attrs", "value",)

    def __init__(self, value=None, methods=False):
        super(Object, self).__init__()

        self.attrs = {}
        self.value = value

        if methods:
            self.create_methods()

    def create_methods(self):
        from closure import Closure
        keys = self.__class__.__dict__.keys()
        predicate = lambda x: ismethod(x) and getattr(x, "method", False)
        for name, method in getmembers(self, predicate):
            if name in keys:
                self[method.name] = Closure(method.name, method, self)

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

    def __str__(self):
        type = self.attrs.get("type",  self.__class__.__name__)
        default = "%s_%s" % (str(type), hex(id(self)))
        return str(self.value) if self.value is not None else default

    __repr__ = __str__

    def clone(self, value=None, type=None):
        obj = copy(self)

        obj.attrs = {}

        obj["parent"] = self

        if value:
            obj.value = value

        if type:
            obj["type"] = type

        return obj

    def forward(self, key):
        return runtime.state.find(key)

    # Attribute Operations

    @method("del")
    def _del(self, receiver, context, m, key):
        key = key(context).value if key.type else key.name
        del receiver[key]
        return runtime.state.find("None")

    @method()
    def has(self, receiver, context, m, key):
        key = key(context).value if key.type else key.name
        if key in receiver:
            return runtime.state.find("True")
        return runtime.state.find("False")

    @method()
    def set(self, receiver, context, m, key, value):
        key = key(context).value if key.type else key.name
        receiver[key] = value
        return value

    @method()
    def get(self, receiver, context, m, key, default=None):
        key = key(context).value if key.type else key.name
        default = default(context) if default else runtime.state.find("None")
        return receiver.attrs.get(key, default)

    # Method Operations

    @method("method")
    def _method(self, receiver, context, m, *args):
        from block import Block
        from closure import Closure

        if m.parent is not None:
            name = m.parent.args[0].name
        else:
            name = ""

        args, expr = args[:-1], args[-1:][0]

        block = Block(None, expr, args)
        return Closure(name, block, receiver)

    # Flow Control

    @method()
    def foreach(self, receiver, context, m, *args):
        result = self["None"]
        runtime.state.reset()

        vars, expression = args[:-1], args[-1]

        for item in receiver:
            if len(vars) == 2:
                context[vars[0].name], context[vars[1].name] = item
            elif len(vars) == 1:
                context[vars[0].name] = item

            result = expression(context)

        runtime.state.reset()
        return result

    @method("while")
    def _while(self, receiver, context, m, condition, expression):
        result = self["None"]

        runtime.state.reset()

        while condition(context).value and (not runtime.state.stop()):
            result = expression(context)

        runtime.state.reset()

        return result

    @method("if")
    def _if(self, receiver, context, m, *args):
        test = bool(args[0](context).value)
        index = 1 if test else 2
        if index < len(args):
            return args[index](context)

        return self["True"] if test else self["False"]

    @method("continue")
    def _continue(self, receiver, context, m):
        runtime.state.isContinue = True
        return self["None"]

    @method("break")
    def _break(self, reciver, context, m, *args):
        value = args[0](context) if args else self["None"]
        runtime.state.isBreak = True
        runtime.state.returnValue = value
        return value

    @method("return")
    def _return(self, reciver, context, m, *args):
        value = args[0](context) if args else self["None"]
        runtime.state.isReturn = True
        runtime.state.returnValue = value
        return value

    # I/O

    @method("print")
    def _print(self, receiver, context, m):
        sys.stdout.write("%s" % self.value)
        return self

    @method()
    def println(self, receiver, context, m):
        sys.stdout.write("%s\n" % self.value)
        return self

    @method()
    def write(self, receiver, context, m, *args):
        sys.stdout.write("%s" % " ".join([str(arg) for arg in args]))
        return self["None"]

    @method()
    def writeln(self, receiver, context, m, *args):
        sys.stdout.write("%s\n" % " ".join([str(arg) for arg in args]))
        return self["None"]

    # Introspection

    @method()
    def type(self, receiver, context, m):
        return self["String"].clone(receiver.__class__.__name__)

    @method()
    def hash(self, receiver, context, m):
        return self["Number"].clone(hash(self))

    @method()
    def id(self, receiver, context, m):
        return self["Number"].clone(id(self))

    @method()
    def keys(self, receiver, context, m):
        return self["List"].clone(self.attrs.keys())

    @method()
    def summary(self, receiver, context, m):
        sys.stdout.write("%s\n" % format_object(receiver))
        return receiver

    # Object Operations

    @method()
    def do(self, receiver, context, m, expression):
        expression(receiver)
        return receiver

    @method()
    def mixin(self, receiver, context, m, other):
        skip = ("parent", "type")
        pairs = ((k, v) for k, v in other.attrs.items() if not k in skip)
        self.attrs.update(pairs)
        return self

    @method("clone")
    def _clone(self, receiver, context, m, *args):
        if m.parent is not None:
            type = self["String"].clone(m.parent.args[0].name)
        else:
            type = None
        cloned = receiver.clone(type=type)
        if "init" in cloned:
            cloned["init"](context, *args)
        return cloned

    # Boolean Operations

    @method()
    def evalArg(self, receiver, context, m, arg):
        return arg

    @method()
    def evalArgAndReturnSelf(self, receiver, context, m, arg):
        return self

    @method()
    def evalArgAndReturnNone(self, receiver, context, m, arg):
        return self["None"]

    @method()
    def eq(self, receiver, context, m, other):
        test = self == other
        return self["True"] if test else self["False"]

    @method()
    def cmp(self, receiver, context, m, other):
        return self["Number"].clone(cmp(self, other))

    @method("and")
    def _and(self, receiver, context, m, other):
        return self.clone(self and other)

    @method("or")
    def _or(self, receiver, context, m, other):
        return self.clone(self or other)

    @method("not")
    def _not(self, receiver, context, m, value=None):
        return value.clone(not value) if value else self.clone(not self)

    # Type Conversion

    @method("str")
    def str(self, receiver, context, m):
        return self["String"].clone(str(self))
