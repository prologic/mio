from inspect import ismethod

import runtime
from object import Object
from utils import format_method, method


class Closure(Object):

    def __init__(self, method, target):
        super(Closure, self).__init__()

        self.method = method
        self.target = target

        self.callable = True

        self["parent"] = runtime.find("Object")
        self["call"] = lambda env: self(env)

    def __str__(self):
        type = self.target.__class__.__name__
        if ismethod(self.method):
            return "%s_%s" % (type, format_method(self.method))
        return "%s_%s" % (type, str(self.method))

    def __call__(self, env):
        try:
            runtime.state.reset()
            return self.method(env)
        finally:
            runtime.state.reset()
