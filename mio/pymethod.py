

class PyMethod(object):

    def __init__(self, method):
        super(PyMethod, self).__init__()

        self.method = method

    def __call__(self, receiver, context, *args):
        args = [arg(context) for arg in args]
        return getattr(receiver, self.method)(*args)

    def __repr__(self):
        return "%s(...)" % self.method


def pymethod(name=None):
    def wrapper(f):
        f.name = name or f.__name__
        f.pymethod = True
        return f

    return wrapper
