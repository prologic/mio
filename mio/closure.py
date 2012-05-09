from inspect import ismethod

import runtime
from object import Object
from errors import ArgsError


class Closure(Object):

    def __init__(self, name, method, receiver):
        super(Closure, self).__init__()

        self.name = name
        self.method = method
        self.receiver = receiver

    def __call__(self, receiver, context, m, *args):
        if ismethod(self.method):
            if not self.method.vargs and not len(args) in self.method.nargs:
                raise ArgsError(len(args), self.method)

        try:
            runtime.state.reset()
            return self.method(receiver, context, m, *args)
        finally:
            runtime.state.reset()
