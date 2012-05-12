import sys
from copy import copy
from inspect import  getmembers, ismethod

import runtime
from errors import KeyError
from utils import format_object, method, Null


class Object(object):

    __slots__ = ("attrs", "callable", "done_lookup", "value",)

    def __init__(self, value=Null, methods=False):
        super(Object, self).__init__()

        self.attrs = {}
        self.value = value

        self.callable = False
        self.done_lookup = False

        if methods:
            self.create_methods()

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        return self.value == getattr(other, "value", other)

    def __cmp__(self, other):
        return cmp(self.value, getattr(other, "value", other))

    def __contains__(self, key):
        return key in self.attrs

    def __delitem__(self, key):
        if key in self.attrs:
            del self.attrs[key]

    def __setitem__(self, key, value):
        self.attrs[key] = value

    def __str__(self):
        type = self.attrs.get("type",  self.__class__.__name__)
        if isinstance(type, Object) and not isinstance(type.value, str):
            type = self.__class__.__name__
        default = "%s_%s" % (str(type), hex(id(self)))
        return str(self.value) if self.value is not Null else default

    __repr__ = __str__

    def clone(self, value=Null, type=None):
        obj = copy(self)

        obj.attrs = {}

        obj["parent"] = self

        if value is not Null:
            obj.value = value

        if type is not None:
            obj["type"] = type

        return obj

    def create_methods(self):
        from closure import Closure
        keys = self.__class__.__dict__.keys()
        predicate = lambda x: ismethod(x) and getattr(x, "method", False)
        for name, method in getmembers(self, predicate):
            if name in keys:
                self[method.name] = Closure(method)

    def lookup(self, env, key):
        def default_lookup(env, key):
            if self.done_lookup:
                return
            obj = self.attrs.get(key)
            if obj is not None:
                return obj
            self.done_lookup = True
            parent = env.target.attrs.get("parent")
            if parent is not None:
                obj = parent.lookup(env, key)
            self.done_lookup = False
            return obj

        lookup = self.attrs.get("lookup", default_lookup)

        if lookup is not None and not self.done_lookup:
            r = lookup(env, key)
            self.done_lookup = False
            return r

    def perform(self, env):
        if env.msg.value is not None:
            return env.msg.value

        obj = self.lookup(env, env.msg.name)
        env.target = self

        if obj is not None:
            if obj.callable:
                call = obj.lookup(env, "call")
                if call is not None:
                    return call(env.update({"scope": self}))
            return obj

        forward = self.lookup(env, "forward")
        if forward is not None:
            forward(env.update({"scope": self}))

        raise KeyError(env.target, env.msg.name)

    def forward(self, key):
        return runtime.state.find(key)

    @method("\n")
    def newline(self, env):
        return env.sender

    @method(";")
    def semicolon(self, env):
        return env.sender

    # Attribute Operations

    @method("del")
    def _del(self, env, key):
        key = key.eval(context).value if key.type else key.name
        del receiver[key]
        return runtime.state.find("None")

    @method()
    def has(self, env, key):
        key = key.eval(context).value if key.type else key.name
        if key in receiver:
            return runtime.state.find("True")
        return runtime.state.find("False")

    @method()
    def set(self, env):
        key, value = env.msg.args
        key = key.value if key.type else key.name
        env.target[key] = value.eval(env)
        return value

    @method()
    def get(self, env):
        if len(env.msg.args) == 2:
            key, default = env.msg.args
        else:
            key, default = env.msg.args[0], runtime.state.find("None")

        key = key.value if key.type else key.name
        return env.target.lookup(env, key)

    # Method/Block Operations

    @method("block")
    def block(self, env, *args):
        from block import Block
        args, expression = args[:-1], args[-1:][0]
        return Block(context, expression, args)

    @method("method")
    def _method(self, env, *args):
        from block import Block
        from closure import Closure
        args, expression = env.msg.args[:-1], env.msg.args[-1:][0]
        return Closure(Block(None, expression, args))

    # Flow Control

    @method()
    def foreach(self, env, *args):
        result = self["None"]
        runtime.state.reset()

        vars, expression = args[:-1], args[-1]

        for item in receiver:
            if len(vars) == 2:
                context[vars[0].name], context[vars[1].name] = item
            elif len(vars) == 1:
                context[vars[0].name] = item

            result = expression.eval(context)

        runtime.state.reset()
        return result

    @method("while")
    def _while(self, env, condition, expression):
        result = self["None"]

        runtime.state.reset()

        while bool(condition.eval(context)) and (not runtime.state.stop()):
            result = expressione.eval(context)

        runtime.state.reset()

        return result

    @method("if")
    def _if(self, env, *args):
        test = bool(args[0].eval(context))
        index = 1 if test else 2
        if index < len(args):
            return args[index].eval(context)

        return self["True"] if test else self["False"]

    @method("continue")
    def _continue(self, env):
        runtime.state.isContinue = True
        return self["None"]

    @method("break")
    def _break(self, reciver, context, m, *args):
        value = args[0].eval(context) if args else self["None"]
        runtime.state.isBreak = True
        runtime.state.returnValue = value
        return value

    @method("return")
    def _return(self, reciver, context, m, *args):
        value = args[0].eval(context) if args else self["None"]
        runtime.state.isReturn = True
        runtime.state.returnValue = value
        return value

    # I/O

    @method("print")
    def _print(self, env):
        sys.stdout.write("%s" % receiver.value)
        return receiver

    @method()
    def println(self, env):
        sys.stdout.write("%s\n" % receiver.value)
        return receiver

    @method()
    def write(self, env, *args):
        args = [arg.eval(context) for arg in args]
        sys.stdout.write("%s" % " ".join([str(arg) for arg in args]))
        return self["None"]

    @method()
    def writeln(self, env, *args):
        args = [arg.eval(context) for arg in args]
        sys.stdout.write("%s\n" % " ".join([str(arg) for arg in args]))
        return self["None"]

    # Introspection

    @method()
    def type(self, env):
        return self["String"].clone(receiver.__class__.__name__)

    @method()
    def hash(self, env):
        return self["Number"].clone(hash(receiver))

    @method()
    def id(self, env):
        return self["Number"].clone(id(receiver))

    @method()
    def keys(self, env):
        return self["List"].clone(receiver.attrs.keys())

    @method()
    def summary(self, env):
        type = str(receiver["type"](env))
        sys.stdout.write("%s\n" % format_object(receiver, type=type))
        return receiver

    # Object Operations

    @method()
    def do(self, env):
        env.msg.eval_arg(env.update({"sender": env.target}), 0)
        return env.target

    @method()
    def mixin(self, env, other):
        skip = ("parent", "type")
        other = other.eval(context)
        pairs = ((k, v) for k, v in other.attrs.items() if not k in skip)
        self.attrs.update(pairs)
        return receiver

    @method("clone")
    def _clone(self, env, *args):
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
    def evalArg(self, env, arg=None):
        return arg.eval(context) if arg else self["None"]

    @method()
    def evalArgAndReturnSelf(self, env, arg=None):
        arg.eval(context)
        return self

    @method()
    def evalArgAndReturnNone(self, env, arg=None):
        arg.eval(context)
        return self["None"]

    @method("==")
    def eq(self, env, other):
        test = receiver == other.eval(context)
        return self["True"] if test else self["False"]

    @method("!=")
    def neq(self, env, other):
        test = not (receiver == other.eval(context))
        return self["True"] if test else self["False"]

    @method()
    def cmp(self, env, other):
        return self["Number"].clone(cmp(receiver, other.eval(context)))

    @method("and")
    def _and(self, env, other):
        return self.clone(receiver and other.eval(context))

    @method("or")
    def _or(self, env, other):
        return self.clone(receiver or other.eval(context))

    @method("not")
    def _not(self, env, value=None):
        if value:
            return value.clone(not value.eval(context))
        return receiver.clone(not receiver)

    # Type Conversion

    @method("str")
    def str(self, env):
        return self["String"].clone(str(receiver))
