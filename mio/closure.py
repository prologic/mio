from inspect import ismethod

import runtime
from object import Object
from errors import ArgsError
from utils import format_method


class Closure(Object):

    def __init__(self, name, method, receiver):
        super(Closure, self).__init__()

        self.name = name
        self.method = method
        self.receiver = receiver

        self.create_methods()

    def __str__(self):
        type = self.receiver.attrs.get("type", 
                self.receiver.__class__.__name__)
        if isinstance(type, Object) and not isinstance(type.value, str):
            type = self.receiver.__class__.__name__

        if ismethod(self.method):
            return "%s_%s" % (type, format_method(self.method))
        return str(self.method)

    def __call__(self, receiver, context, m, *args):
        if ismethod(self.method):
            if not self.method.vargs and not len(args) in self.method.nargs:
                raise ArgsError(len(args), self.method)

        try:
            runtime.state.reset()
            return self.method(receiver, context, m, *args)
        finally:
            runtime.state.reset()
