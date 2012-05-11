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

        self.callable = True

        self.create_methods()
        self["parent"] = runtime.state.find("Object")

    def __call__(self, env):
        self.create_locals(env, self.scope)
        for i, arg in enumerate(self.args):
            self.locals[arg] = env.msg.eval_arg(i)
        return self.body.perform_on(env, self.locals, self.locals)

    def create_locals(self, env, parent):
        self.locals = Locals()

        if parent is not None:
            self.locals["parent"] = parent
        else:
            self.locals["parent"] = env.target

        if self.scope is not None:
            self.locals["self"] = self.scope
        else:
            self.locals["self"] = env.target

        call = Call()
        call["parent"] = runtime.state.find("Object")

        call["message"] = env.msg
        call["target"] = env.target
        call["sender"] = env.sender

        self.locals["call"] = call

    @method()
    def call(self, env):
        return self(env)

    @method("args")
    def _args(self, env):
        return self["List"].clone(self.args)

    @method("body")
    def _body(self, env):
        return self.body

    @method("scope")
    def _scope(self, env):
        return self.scope if self.scope is not None else self["None"]
