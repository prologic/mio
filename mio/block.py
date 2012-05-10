import runtime
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
        self.args = args

        self.locals = None

        self.create_methods()
        self["parent"] = runtime.state.find("Object")

    def create_locals(self, receiver, context, m, parent):
        if self.locals is None:
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

        for i, arg in enumerate(self.args):
            if i < len(args):
                self.locals[arg.name] = args[i](context)
            else:
                self.locals[arg.name] = self["None"](context)

        return self.body(self.locals)
