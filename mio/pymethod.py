from inspect import getargspec

from errors import ArgsError
from utils import format_method


def pymethod(name=None):
    def wrapper(f):
        f.name = name or f.__name__
        f.type = "python"
        f.method = True

        argspec = getargspec(f)
        args = argspec.args
        varargs = argspec.varargs
        defaults = argspec.defaults or ()

        for arg in ("self", "receiver", "context",):
            if args and args[0] == arg:
                del args[0]

        max_args = len(args)
        min_args = max_args - len(defaults)
        f.nargs = range(min_args, (max_args + 1))

        f.args = args
        f.vargs = varargs
        f.dargs = defaults

        return f

    return wrapper


class PyMethod(object):

    def __init__(self, method):
        super(PyMethod, self).__init__()

        self.method = method

    def __call__(self, receiver, context, m, *args):
        if not self.method.vargs and not len(args) in self.method.nargs:
            raise ArgsError(len(args), self.method)

        method = self.method.__name__
        args = [arg(context) for arg in args]
        return getattr(receiver, method)(*args)

    def __repr__(self):
        return format_method(self.method)
