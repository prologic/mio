import runtime
from utils import method

from object import Object


class Call(Object):
    """Call Object"""


class Locals(Object):
    """Locals Object"""


class Block(Object):

    def __init__(self, scope, body, args):
        super(Block, self).__init__()

        self.scope = scope
        self.body = body
        self.args = [arg.name for arg in args]

        self.locals = None

        self.create_methods()
        self["parent"] = runtime.state.find("Object")

    def __str__(self):
        args = ",".join(self.args)
        return "method(%s)" % args

    def create_locals(self, receiver, context, m, parent):
        self.locals = Locals()

        if parent is not None:
            self.locals["parent"] = parent
        else:
            self.locals["parent"] = receiver

        if self.scope is not None:
            self.locals["self"] = self.scope
        else:
            self.locals["self"] = receiver

        call = Call()
        call["parent"] = runtime.state.find("Object")

        call["message"] = m
        call["target"] = receiver
        call["sender"] = context

        self.locals["call"] = call

    def __call__(self, receiver, context=None, m=None, *args):
        self.create_locals(receiver, context, m, self.scope)

        args = [arg.eval(context) for arg in args]

        for i, arg in enumerate(self.args):
            self.locals[arg] = args[i] if i < len(args) else self["None"]

        try:
            runtime.state.reset()
            return self.body.eval(self.locals, self.locals)
        finally:
            runtime.state.reset()

    @method("args")
    def _args(self, receiver, context, m):
        return self["List"].clone(self.args)

    @method("body")
    def _body(self, receiver, context, m):
        return self.body

    @method("scope")
    def _scope(self, receiver, context, m):
        return self.scope if self.scope is not None else self["None"]
