from inspect import ismethod

import runtime
from object import Object
from utils import format_method, method


class Closure(Object):

    def __init__(self, name, method, receiver):
        super(Closure, self).__init__()

        self.name = name
        self.method = method
        self.receiver = receiver

        self.callable = True

        self["call"] = lambda env: self(env)

    def __str__(self):
        if ismethod(self.method):
            return format_method(self.method)
        return str(self.method)

    def __call__(self, env):
        try:
            runtime.state.reset()
            return self.method(env, *env.msg.eval_args(env))
        finally:
            runtime.state.reset()
