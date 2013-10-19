from __future__ import print_function

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

    def __str__(self):
        args = ",".join(self.args)
        return "{0:s}({1:s})\n{2:s}".format("block" if self.scope is not None else "method", args, repr(self.body))

    __repr__ = __str__

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

        for arg in args:
            if arg.name == "set":
                arg.eval(self.locals, context)

        for i, arg in enumerate(self.args):
            if i < len(args):
                self.locals[arg] = args[i].eval(context)
            else:
                self.locals[arg] = runtime.find("None")

        if runtime.state.opts and runtime.state.opts.debug:
            print("Calling {0:s} with args={1:s} and kwargs={2:s} and body={3:s}".format(repr(self), repr(self.args), repr(self.kwargs), repr(self.body)))

        try:
            returnValue = self.body.eval(self.locals, self.locals)
            if runtime.state.opts and runtime.state.opts.debug:
                print("Return {0:s}".format(repr(returnValue)))
            return returnValue
        finally:
            context.state = NormalState()

    @method("args")
    def _args(self, receiver, context, m):
        return self["List"].clone(self.args)

    @method("body")
    def _body(self, receiver, context, m):
        return self.body
