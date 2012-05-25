import sys
from copy import copy
from inspect import  getmembers, ismethod

import runtime
from errors import AttributeError
from utils import format_object, pymethod, Null


class Object(object):

    __slots__ = ("attrs", "value", "traits", "behaviors",)

    def __init__(self, value=Null, methods=False):
        super(Object, self).__init__()

        self.attrs = {}
        self.value = value

        self.traits = []
        self.behaviors = {}

        if methods:
            self.create_methods()

    def create_methods(self):
        keys = self.__class__.__dict__.keys()
        predicate = lambda x: ismethod(x) and getattr(x, "pymethod", False)
        for name, method in getmembers(self, predicate):
            if name in keys:
                self[method.name] = method

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
            parent = self.attrs.get("parent")
            while parent is not None:
                if key in parent:
                    return parent[key]
                parent = parent.attrs.get("parent")

        if hasattr(self, "forward"):
            try:
                return self.forward(key)
            except:
                raise AttributeError("%s has no attribute %r" % (self, key))
        raise AttributeError("%s has no attribute %r" % (self, key))

    def __setitem__(self, key, value):
        self.attrs[key] = value

    def __addtrait__(self, trait):
        for k, v in trait.attrs.items():
            self.behaviors[k] = v
        self.traits.append(trait)

    def __deltrait__(self, trait):
        for k, v in trait.attrs.items():
            del self.behaviors[k]
        self.traits.remvoe(trait)

    def __call__(self, *args, **kwargs):
        return self

    def __str__(self):
        return str(self.value) if self.value is not Null else self.type

    __repr__ = __str__

    def clone(self, value=Null):
        obj = copy(self)

        obj.attrs = {}

        obj["parent"] = self

        if value is not Null:
            obj.value = value

        return obj

    def forward(self, key):
        return runtime.state.find(key)

    @property
    def type(self):
        return self.__class__.__name__

    # Attribute Operations

    @pymethod("del")
    def _del(self, receiver, context, m, key):
        key = key.eval(context)
        del receiver[key]
        return runtime.state.find("None")

    @pymethod()
    def has(self, receiver, context, m, key):
        key = key.eval(context)
        if key in receiver:
            return runtime.state.find("True")
        return runtime.state.find("False")

    @pymethod()
    def set(self, receiver, context, m, key, value):
        key = key.eval(context)
        value = value.eval(context)
        receiver[key] = value
        return value

    @pymethod()
    def get(self, receiver, context, m, key, default=None):
        key = key.eval(context)
        default = default.eval(context) if default else runtime.find("None")
        return receiver.attrs.get(key, default)

    # Traits Operations

    @pymethod()
    def uses(self, receiver, context, m, *traits):
        traits = [trait.eval(context) for trait in traits]
        for trait in traits:
            receiver.__addtrait__(trait)
        return receiver

    @pymethod()
    def addTrait(self, receiver, context, m, trait):
        trait = trait.eval(context)
        receiver.__addtrait__(trait)
        return receiver

    @pymethod()
    def delTrait(self, receiver, context, m, trait):
        trait = trait.eval(context)
        receiver.__deltrait__(trait)
        return receiver

    @pymethod()
    def hasTrait(self, receiver, context, m, trait):
        trait = trait.eval(context)
        test = trait in receiver.traits
        return runtime.find("True") if test else runtime.find("False")

    @pymethod("traits")
    def getTraits(self, receiver, context, m):
        return runtime.find("List").clone(receiver.traits)

    @pymethod("behaviors")
    def getBehaviors(self, receiver, context, m):
        keys = receiver.behaviors.keys()
        return runtime.find("List").clone(receiver.behaviors.keys())

    # Method Operations

    @pymethod()
    def method(self, receiver, context, m, *args):
        scope = context if "call" in context else None
        args, body = args[:-1], args[-1:][0]

        method = runtime.find("Method").clone()

        method.args = [arg.name for arg in args]
        method.scope = scope
        method.body = body

        return method

    # Flow Control

    @pymethod()
    def foreach(self, receiver, context, m, *args):
        result = runtime.find("None")
        runtime.state.reset()

        vars, expression = args[:-1], args[-1]

        for item in receiver:
            if runtime.state.isContinue:
                runtime.state.reset()
                continue

            if len(vars) == 2:
                context[vars[0].name], context[vars[1].name] = item
            elif len(vars) == 1:
                context[vars[0].name] = item

            result = expression.eval(context)

            if runtime.state.stop():
                return runtime.state.returnValue

        try:
            return result
        finally:
            runtime.state.reset()

    @pymethod("while")
    def _while(self, receiver, context, m, condition, expression):
        result = runtime.find("None")

        runtime.state.reset()

        while condition.eval(context) and (not runtime.state.stop()):
            result = expression.eval(context)

        runtime.state.reset()

        return result

    @pymethod("if")
    def _if(self, receiver, context, m, *args):
        test = args[0].eval(context)
        index = 1 if test else 2
        if index < len(args):
            return args[index].eval(context)

        return runtime.find("True") if test else runtime.find("False")

    @pymethod("continue")
    def _continue(self, receiver, context, m):
        runtime.state.isContinue = True
        return runtime.find("None")

    @pymethod("break")
    def _break(self, reciver, context, m, *args):
        value = args[0].eval(context) if args else runtime.find("None")
        runtime.state.isBreak = True
        runtime.state.returnValue = value
        return value

    @pymethod("return")
    def _return(self, reciver, context, m, *args):
        value = args[0].eval(context) if args else runtime.find("None")
        runtime.state.isReturn = True
        runtime.state.returnValue = value
        return value

    # I/O

    @pymethod("print")
    def _print(self, receiver, context, m):
        sys.stdout.write("%s" % receiver.value)
        return receiver

    @pymethod()
    def println(self, receiver, context, m):
        sys.stdout.write("%s\n" % receiver.value)
        return receiver

    @pymethod()
    def write(self, receiver, context, m, *args):
        args = [arg.eval(context) for arg in args]
        sys.stdout.write("%s" % " ".join([str(arg) for arg in args]))
        return runtime.find("None")

    @pymethod()
    def writeln(self, receiver, context, m, *args):
        args = [arg.eval(context) for arg in args]
        sys.stdout.write("%s\n" % " ".join([str(arg) for arg in args]))
        return runtime.find("None")

    # Introspection

    @pymethod("type")
    def _type(self, receiver, context, m):
        return runtime.find("String").clone(receiver.type)

    @pymethod()
    def hash(self, receiver, context, m):
        return runtime.find("Number").clone(hash(receiver))

    @pymethod()
    def id(self, receiver, context, m):
        return runtime.find("Number").clone(id(receiver))

    @pymethod()
    def keys(self, receiver, context, m):
        String = runtime.find("String")
        keys = [String.clone(key) for key in receiver.attrs.keys()]
        return runtime.find("List").clone(keys)

    @pymethod()
    def summary(self, receiver, context, m):
        sys.stdout.write("%s\n" % format_object(receiver, receiver.type))
        return receiver

    # Object Operations

    @pymethod()
    def do(self, receiver, context, m, expression):
        expression.eval(receiver)
        return receiver

    @pymethod()
    def super(self, receiver, context, m):
        return receiver["self"]["parent"]

    @pymethod("clone")
    def _clone(self, receiver, context, m, *args):
        object = receiver.clone()

        try:
            m = runtime.find("Message").clone()
            m.name = "init"
            m.args = args
            m.eval(object, context)
        except AttributeError:
            pass

        return object

    # Boolean Operations

    @pymethod()
    def evalArg(self, receiver, context, m, arg=None):
        if arg is not None:
            return arg.eval(context)
        else:
            return runtime.find("None")

    @pymethod()
    def evalArgAndReturnSelf(self, receiver, context, m, arg=None):
        arg.eval(context)
        return self

    @pymethod()
    def evalArgAndReturnNone(self, receiver, context, m, arg=None):
        arg.eval(context)
        return runtime.find("None")

    @pymethod("==")
    def eq(self, receiver, context, m, other):
        test = receiver == other.eval(context)
        return runtime.find("True") if test else runtime.find("False")

    @pymethod("!=")
    def neq(self, receiver, context, m, other):
        test = not (receiver == other.eval(context))
        return runtime.find("True") if test else runtime.find("False")

    @pymethod()
    def cmp(self, receiver, context, m, other):
        return runtime.find("Number").clone(cmp(receiver, other.eval(context)))

    @pymethod("and")
    def _and(self, receiver, context, m, other):
        return self.clone(receiver and other.eval(context))

    @pymethod("or")
    def _or(self, receiver, context, m, other):
        return self.clone(receiver or other.eval(context))

    @pymethod("not")
    def _not(self, receiver, context, m, value=None):
        value = value.eval(context) if value is not None else receiver
        test = not bool(value)
        return runtime.find("True") if test else runtime.find("False")

    # Type Conversion

    @pymethod("str")
    def str(self, receiver, context, m):
        return runtime.find("String").clone(str(receiver))
