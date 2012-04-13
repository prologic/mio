from inspect import getargspec

from mio.errors import ArgsError

class PyMethod(object):

    def __init__(self, method):
        super(PyMethod, self).__init__()

        self.method = method

    def __call__(self, receiver, context, *args):
        if not len(args) == len(self.method.args):
            raise ArgsError(len(self.method.args), len(args))

        method = self.method.__name__
        args = [arg(context) for arg in args]
        return getattr(receiver, method)(*args)

    def __repr__(self):
        name = self.method.name

        if self.method.args:
            args = ", ".join(self.method.args)
        else:
            args = "..."

        return "%s(%s)" % (name, args)


def pymethod(name=None):
    def wrapper(f):
        f.name = name or f.__name__
        f.pymethod = True

        args = getargspec(f)[0]

        for arg in ("self", "receiver", "context",):
            if args and args[0] == arg:
                del args[0]

        f.args = args

        return f

    return wrapper
