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
    def _del(self, env):
        key = env.msg.args[0]
        key = key.value if key.type else key.name
        del env.target[key]
        return runtime.state.find("None")

    @method()
    def has(self, env, key):
        key = env.msg.args[0]
        key = key.value if key.type else key.name
        if key in env.target:
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
    def block(self, env):
        from block import Block
        args = env.msg.args
        args, expression = args[:-1], args[-1:][0]
        return Block(env.target, expression, args)

    @method("method")
    def _method(self, env, *args):
        from block import Block
        from closure import Closure
        args, expression = env.msg.args[:-1], env.msg.args[-1:][0]
        return Closure(Block(None, expression, args))

    # Flow Control

    @method()
    def foreach(self, env, *args):
        result = runtime.find("None")
        runtime.state.reset()

        vars, expression = args[:-1], args[-1]

        for item in env.target:
            if len(vars) == 2:
                context[vars[0].name], context[vars[1].name] = item
            elif len(vars) == 1:
                context[vars[0].name] = item

            result = expression.eval(context)

        runtime.state.reset()
        return result

    @method("while")
    def _while(self, env, condition, expression):
        result = runtime.find("None")

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

        return runtime.find("True") if test else runtime.find("False")

    @method("continue")
    def _continue(self, env):
        runtime.state.isContinue = True
        return runtime.find("None")

    @method("break")
    def _break(self, reciver, context, m, *args):
        value = args[0].eval(context) if args else runtime.find("None")
        runtime.state.isBreak = True
        runtime.state.returnValue = value
        return value

    @method("return")
    def _return(self, reciver, context, m, *args):
        value = args[0].eval(context) if args else runtime.find("None")
        runtime.state.isReturn = True
        runtime.state.returnValue = value
        return value

    # I/O

    @method("print")
    def _print(self, env):
        sys.stdout.write("%s" % env.target)
        return env.target

    @method()
    def println(self, env):
        sys.stdout.write("%s\n" % env.target)
        return env.target

    @method()
    def write(self, env, *args):
        args = [arg.eval(context) for arg in args]
        sys.stdout.write("%s" % " ".join([str(arg) for arg in args]))
        return runtime.find("None")

    @method()
    def writeln(self, env, *args):
        args = [arg.eval(context) for arg in args]
        sys.stdout.write("%s\n" % " ".join([str(arg) for arg in args]))
        return runtime.find("None")

    # Introspection

    @method()
    def type(self, env):
        return runtime.find("String").clone(env.target.__class__.__name__)

    @method()
    def hash(self, env):
        return runtime.find("Number").clone(hash(env.target))

    @method()
    def id(self, env):
        return runtime.find("Number").clone(id(env.target))

    @method()
    def keys(self, env):
        return runtime.find("List").clone(env.target.attrs.keys())

    @method()
    def summary(self, env):
        type = env.target.lookup(env, "type")
        sys.stdout.write("%s\n" % format_object(env.target, type=type))
        return env.target

    # Object Operations

    @method()
    def do(self, env):
        env.msg.args[0].perform_on(env, env.sender, env.target)
        return env.target

    @method()
    def mixin(self, env):
        skip = ("parent", "type")
        other = env.msg.eval_arg(env, 0)
        pairs = ((k, v) for k, v in other.attrs.items() if not k in skip)
        self.attrs.update(pairs)
        return env.target

    @method("clone")
    def _clone(self, env):
        if env.msg.parent is not None:
            type = runtime.find("String").clone(env.msg.parent.args[0].name)
        else:
            type = None

        cloned = env.target.clone(type=type)

        if "init" in cloned:
            from message import Message
            msg = Message("init", *env.msg.eval_args(env))
            clonded.perform(env.update({"msg": msg}))

        return cloned

    # Boolean Operations

    @method()
    def evalArg(self, env):
        return env.msg.eval_arg(env, 0)

    @method()
    def evalArgAndReturnSelf(self, env, arg=None):
        arg.eval(context)
        return self

    @method()
    def evalArgAndReturnNone(self, env, arg=None):
        arg.eval(context)
        return runtime.find("None")

    @method("==")
    def eq(self, env):
        test = env.target == env.msg.eval_arg(env, 0)
        return runtime.find("True") if test else runtime.find("False")

    @method("!=")
    def neq(self, env):
        test = not (env.target == env.msg.eval_arg(env, 0))
        return runtime.find("True") if test else runtime.find("False")

    @method()
    def cmp(self, env):
        result = cmp(env.target, env.msg.eval_arg(env, 0))
        return runtime.find("Number").clone(result)

    @method("and")
    def _and(self, env):
        return self.clone(env.target and env.msg.eval_arg(env, 0))

    @method("or")
    def _or(self, env):
        return self.clone(env.target or env.msg.eval_arg(env, 0))

    @method("not")
    def _not(self, env):
        if env.msg.args:
            value = env.msg.eval_arg(env, 0)
            return value.clone(not value)
        return env.target.clone(not env.target)

    # Type Conversion

    @method("str")
    def str(self, env):
        return runtime.find("String").clone(str(env.target))
