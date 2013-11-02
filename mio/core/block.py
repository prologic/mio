from __future__ import print_function

from itertools import chain
from operator import attrgetter


from mio import runtime
from mio.object import Object
from mio.utils import method, Null


def getargname(arg):
    if arg.name == "*" and arg.args:
        return "*{0:s}".format(arg.args[0])
    elif arg.name == "**" and arg.args:
        return "**{0:s}".format(arg.args[0])
    else:
        return arg.name


class Call(Object):
    """Call Object"""


class Locals(Object):
    """Locals Object"""

    def __init__(self, value=Null):
        super(Locals, self).__init__(value=value)

        self.parent = runtime.find("Object")


class Block(Object):

    def __init__(self, body=None, args=None, kwargs=None, scope=None):
        super(Block, self).__init__()

        self.body = body if body is not None else self
        self.args = args if args is not None else ()
        self.kwargs = kwargs if kwargs is not None else {}

        self.scope = scope

        self.locals = None

        self.create_methods()
        self.parent = runtime.find("Object")

    def __repr__(self):
        args = ", ".join(chain(map(getargname, self.args), ("{0:s}={1:s}".format(str(k), repr(v)) for k, v in self.kwargs.items())))
        return "{0:s}({1:s})".format("block" if self.scope is not None else "method", args)

    def create_locals(self, receiver, context, m):
        self.locals = Locals()

        if self.scope is None:
            self.locals["self"] = receiver
            self.locals.parent = receiver
        elif isinstance(self.scope, Locals):
            self.locals["self"] = self.scope
            self.locals.parent = self.scope
        else:
            self.locals.parent = runtime.find("Object")

        call = Call()
        call.parent = runtime.find("Object")

        call["message"] = m
        call["target"] = receiver
        call["sender"] = context

        self.locals["call"] = call

    def __call__(self, receiver, context=None, m=None, *args):
        if not m.call:
            return self

        self.create_locals(receiver, context, m)

        self.locals.attrs.update(self.kwargs)

        # Set positional arguments *args
        if len(self.args) == 1 and self.args[0].name == "*":
            self.locals[self.args[0].args[0].name] = runtime.find("List").clone([arg.eval(context) for arg in args if (arg.name != "set" and not arg.args)])
        else:
            # Set positional arguments
            for i, arg in enumerate(self.args):
                if i < len(args):
                    self.locals[arg.name] = args[i].eval(context)
                else:
                    self.locals[arg.name] = runtime.find("None")

        # Set keyword argumetns **kwargs
        if "**" in [arg.name for arg in self.args]:
            i = [arg.name for arg in self.args].index("**")
            d = {}
            for arg in [arg for arg in args if arg.name == "set"]:
                d[arg.args[0].name] = arg.eval(context)
            self.locals[self.args[i].args[0].name] = runtime.find("Dict").clone(d)
        else:
            # Set default keyword argumetns
            for k, v in self.kwargs.items():
                self.locals[k] = v

            # Set keyword arguments
            for arg in [arg for arg in args if arg.name == "set"]:
                self.locals[arg.args[0].name] = arg.eval(context)

        return self.body.eval(self.locals, self.locals)

    @method("args")
    def get_args(self, receiver, context, m):
        return runtime.find("List").clone(map(attrgetter("name"), receiver.args))

    @method("kwargs")
    def get_kwargs(self, receiver, context, m):
        return runtime.find("Dict").clone(receiver.kwargs)

    @method("body")
    def get_body(self, receiver, context, m):
        return receiver.body
