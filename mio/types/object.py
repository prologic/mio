import sys
from copy import copy
from collections import OrderedDict
from inspect import getmembers, ismethod


from mio import runtime
from mio.states import NormalState
from mio.errors import AttributeError, TypeError
from mio.utils import format_object, method, Null
from mio.states import BreakState, ContinueState, ReturnState


class Object(object):

    __slots__ = ("attrs", "binding", "parent", "state", "value", "traits", "behaviors",)

    def __init__(self, value=Null, methods=True):
        super(Object, self).__init__()

        self.attrs = {}
        self.parent = None
        self.value = value

        self.traits = []
        self.behaviors = {}

        self.binding = None
        self.state = NormalState()

        if methods:
            self.create_methods()

    def create_methods(self):
        keys = self.__class__.__dict__.keys()
        self.attrs.update(((v.name, v) for k, v in getmembers(self, ismethod) if getattr(v, "method", False) and k in keys))

    def __hash__(self):
        return hash(self.value)

    def __nonzero__(self):
        return bool(self.value)

    def __eq__(self, other):
        return self.value == getattr(other, "value", other)

    def __cmp__(self, other):
        return cmp(self.value, getattr(other, "value", other))

    def __contains__(self, key):
        return key in self.attrs or key in self.behaviors

    def __delitem__(self, key):
        if key in self.attrs:
            del self.attrs[key]
        elif key in self.behaviors:
            del self.behaviors[key]

    def __getitem__(self, key):
        if key in self.attrs:
            return self.attrs[key]
        elif key in self.behaviors:
            return self.behaviors[key]
        else:
            parent = self.parent
            while parent is not None:
                if key in parent:
                    return parent[key]
                parent = parent.parent

        try:
            return self.forward(key)
        except:
            raise AttributeError("{0:s} has no attribute {1:s}".format(self.type, repr(key)))

    def __setitem__(self, key, value):
        self.attrs[key] = value

    def __addtrait__(self, trait):
        attrs = ((k, v) for k, v in trait.attrs.items())
        methods = ((k, v) for k, v in attrs if v.type == "Block")
        behaviors = ((k, v) for k, v in methods if not k in self.attrs)

        self.behaviors.update(behaviors)
        self.traits.append(trait)

    def __deltrait__(self, trait):
        for k, v in trait.attrs.items():
            del self.behaviors[k]
        self.traits.remove(trait)

    def __repr__(self):
        type = "{0:s}({1:s})".format(self.binding, self.type) if self.binding is not None else self.type
        default = "{0:s} at {1:s}".format(type, hex(id(self)))
        return repr(self.value) if self.value is not Null else default

    def clone(self, value=Null):
        obj = copy(self)

        obj.attrs = {}
        obj.parent = self
        obj.value = value if value is not Null else obj.value

        obj.traits = []
        obj.behaviors = {}

        obj.state = NormalState()

        return obj

    def forward(self, key):
        return runtime.find(key)

    @property
    def type(self):
        return self.__class__.__name__

    # Attribute Operations

    @method("del")
    def _del(self, receiver, context, m, key):
        key = key.eval(context)
        del receiver[key]
        return runtime.find("None")

    @method()
    def has(self, receiver, context, m, key):
        key = key.eval(context)
        if key in receiver:
            return runtime.find("True")
        return runtime.find("False")

    @method()
    def set(self, receiver, context, m, key, value):
        key = key.eval(context)
        value = value.eval(context)
        receiver[key] = value
        return value

    @method()
    def get(self, receiver, context, m, key, default=None):
        key = key.eval(context)
        default = default.eval(context) if default else runtime.find("None")
        return receiver.attrs.get(key, default)

    # Traits Operations

    @method()
    def uses(self, receiver, context, m, *traits):
        traits = [trait.eval(context) for trait in traits]
        for trait in traits:
            receiver.__addtrait__(trait)
        return receiver

    @method()
    def addTrait(self, receiver, context, m, trait):
        trait = trait.eval(context)
        receiver.__addtrait__(trait)
        return receiver

    @method()
    def delTrait(self, receiver, context, m, trait):
        trait = trait.eval(context)
        receiver.__deltrait__(trait)
        return receiver

    @method()
    def hasTrait(self, receiver, context, m, trait):
        trait = trait.eval(context)
        test = trait in receiver.traits
        return runtime.find("True") if test else runtime.find("False")

    @method("traits")
    def getTraits(self, receiver, context, m):
        return runtime.find("List").clone(receiver.traits)

    @method("behaviors")
    def getBehaviors(self, receiver, context, m):
        return runtime.find("List").clone(receiver.behaviors.keys())

    # Block Operations

    @method()
    def block(self, receiver, context, m, *args):
        args, body = args[:-1], args[-1:][0]

        # Evaluate kwargs first
        ctx = runtime.find("Object").clone()
        kwargs = OrderedDict([(arg.args[0].name, arg.eval(ctx)) for arg in args if arg.name == "set"])

        args = [arg for arg in args if not arg.name == "set"]

        from mio.core.block import Block
        return Block(body, args, kwargs, context)

    @method("method")
    def _method(self, receiver, context, m, *args):
        args, body = args[:-1], args[-1:][0]

        # Evaluate kwargs first
        ctx = runtime.find("Object").clone()
        kwargs = OrderedDict([(arg.args[0].name, arg.eval(ctx)) for arg in args if arg.name == "set"])

        args = [arg for arg in args if not arg.name == "set"]

        from mio.core.block import Block
        return Block(body, args, kwargs)

    # Flow Control

    @method()
    def foreach(self, receiver, context, m, *args):
        try:
            result = runtime.find("None")
            vars, expression = args[:-1], args[-1]

            for item in receiver:
                if len(vars) == 2:
                    context[vars[0].name], context[vars[1].name] = item
                elif len(vars) == 1:
                    context[vars[0].name] = item

                result = expression.eval(context)

                if context.state.stop:
                    if context.state.isContinue:
                        context.state = NormalState()
                        continue
                    else:
                        return context.state.returnValue
            return result
        finally:
            if not context.state.isReturn:
                context.state = NormalState()

    @method("while")
    def _while(self, receiver, context, m, condition, expression):
        try:
            result = runtime.find("None")

            while condition.eval(context):
                result = expression.eval(context)

                if context.state.stop:
                    if context.state.isContinue:
                        context.state = NormalState()
                        continue
                    else:
                        return context.state.returnValue
            return result
        finally:
            if not context.state.isReturn:
                context.state = NormalState()

    @method("continue")
    def _continue(self, receiver, context, m):
        context.state = ContinueState()
        return runtime.find("None")

    @method("break")
    def _break(self, reciver, context, m):
        context.state = BreakState()
        return runtime.find("None")

    @method("return")
    def _return(self, receiver, context, m, *args):
        value = args[0].eval(context) if args else runtime.find("None")
        context.state = ReturnState(value)
        return receiver

    # Introspection

    @method("type")
    def getType(self, receiver, context, m):
        return runtime.find("String").clone(receiver.type)

    @method("parent")
    def _parent(self, receiver, context, m):
        if receiver.parent is not None:
            return receiver.parent
        return receiver

    @method("value")
    def _value(self, receiver, context, m):
        if receiver.value is not Null:
            return receiver.value
        return runtime.find("None")

    @method()
    def hash(self, receiver, context, m):
        return runtime.find("Number").clone(hash(receiver))

    @method()
    def id(self, receiver, context, m):
        return runtime.find("Number").clone(id(receiver))

    @method()
    def keys(self, receiver, context, m):
        String = runtime.find("String")
        keys = [String.clone(key) for key in receiver.attrs.keys()]
        return runtime.find("List").clone(keys)

    @method()
    def summary(self, receiver, context, m):
        sys.stdout.write("%s\n" % format_object(receiver))
        return receiver

    # Object Operations

    @method(":")
    def primitive(self, receiver, context, m, method, *args):
        method = method.name
        args = [arg.eval(context).value for arg in args]
        if hasattr(receiver, method):
            return runtime.state.tomio(getattr(receiver, method)(*args))
        raise AttributeError("{0:s} has no attribute {1:s}".format(receiver.type, repr(method)))

    @method()
    def evalArg(self, receiver, context, m, arg):
        return arg.eval(receiver, context)

    @method()
    def do(self, receiver, context, m, expression):
        expression.eval(receiver)
        return receiver

    @method("clone")
    def _clone(self, receiver, context, m, *args):
        object = receiver.clone()

        if m.first.previous.name == "set":
            object.binding = m.first.previous.args[0].name

        try:
            m = runtime.find("Message").clone()
            m.name = "init"
            m.args = args
            m.eval(object, context, m)
        except AttributeError:
            pass

        return object

    @method()
    def setParent(self, receiver, context, m, parent):
        parent = parent.eval(context)
        if parent is receiver:
            raise TypeError("Canoot set parent to self!")

        receiver.parent = parent

        return receiver

    @method()
    def setValue(self, receiver, context, m, value):
        receiver.value = value.eval(context)
        return receiver

    # Boolean Operations

    @method()
    def cmp(self, receiver, context, m, other):
        return runtime.find("Number").clone(cmp(receiver, other.eval(context)))

    # Type Conversion

    @method("repr")
    def repr(self, receiver, context, m):
        return runtime.find("String").clone(repr(receiver))

    @method("str")
    def str(self, receiver, context, m):
        return runtime.find("String").clone(str(receiver))