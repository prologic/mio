import runtime
from utils import method

from object import Object


class Call(Object):
    """Call Object"""


class Locals(Object):
    """Locals Object"""


class Method(Object):

    def __init__(self, scope, body, args, kwargs):
        super(Method, self).__init__()

        self.scope = scope
        self.body = body

        self.args = args
        self.kwargs = kwargs

        self.locals = None

        self.create_methods()
        self.parent = runtime.state.find("Object")

    def __str__(self):
        args = ",".join(self.args)
        return "method(%s)" % args

    def create_locals(self, receiver, context, m):
        self.locals = Locals()

        if self.scope is not None:
            self.locals["self"] = self.scope
            self.locals.parent = self.scope
        else:
            self.locals["self"] = receiver
            self.locals.parent = receiver

        call = Call()
        call["method"] = self
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
