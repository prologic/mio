from __future__ import print_function

from itertools import chain


import runtime
from .utils import method
from .object import Object
from .states import NormalState


class Call(Object):
    """Call Object"""


class Locals(Object):
    """Locals Object"""


class Block(Object):

    def __init__(self, body, args, kwargs, scope=None):
        super(Block, self).__init__()

        self.body = body
        self.args = args
        self.kwargs = kwargs

        self.scope = scope

        self.locals = None

        self.create_methods()
        self.parent = runtime.state.find("Object")

    def __repr__(self):
        args = ", ".join(chain(self.args, ("{0:s}={1:s}".format(str(k), repr(v)) for k, v in self.kwargs.items())))
        return "{0:s}({1:s})".format("block" if self.scope is not None else "method", args)

    def create_locals(self, receiver, context, m):
        self.locals = Locals()

        if self.scope is not None:
            self.locals["self"] = self.scope
            self.locals.parent = self.scope
        else:
            self.locals["self"] = receiver
            self.locals.parent = receiver

        call = Call()
        call.parent = runtime.state.find("Object")

        call["message"] = m
        call["target"] = receiver
        call["sender"] = context

        self.locals["call"] = call

    def __call__(self, receiver, context=None, m=None, *args):
        self.create_locals(receiver, context, m)

        self.locals.attrs.update(self.kwargs)

        # Set positional arguments
        for i, arg in enumerate(self.args):
            if i < len(args):
                self.locals[arg] = args[i].eval(context)
            else:
                self.locals[arg] = runtime.find("None")

        # Set default keyword argumetns
        for k, v in self.kwargs.items():
            self.locals[k] = v

        # Set keyword argumetns
        for arg in [arg for arg in args if arg.name == "set"]:
            self.locals[arg.args[0].name] = arg.eval(context)

        try:
            return self.body.eval(self.locals, self.locals)
        finally:
            context.state = NormalState()

    @method("args")
    def get_args(self, receiver, context, m):
        return runtime.find("List").clone(receiver.args)

    @method("kwargs")
    def get_kwargs(self, receiver, context, m):
        return runtime.find("Dict").clone(receiver.kwargs)

    @method("body")
    def get_body(self, receiver, context, m):
        return receiver.body
