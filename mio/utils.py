from warnings import warn
from threading import RLock
from functools import partial
from inspect import getargspec, ismethod


def format_method(f):
    name = getattr(f, "name", getattr(f, "__name__"))
    argspec = getargspec(f)
    args = list(argspec.args)
    varargs = argspec.varargs
    for arg in ("self", "receiver", "context", "m"):
        if arg in args:
            del args[0]
    args = ", ".join(args) if args else ("*%s" % varargs if varargs else "")
    return "%s(%s)" % (name, args)


def format_object(o):
    attrs = "\n".join(["  {0:s} = {1:s}".format(str(k).ljust(15), format_method(v) if ismethod(v) else repr(v)) for k, v in sorted(o.attrs.items())])
    return "{0:s}:\n{1:s}".format(o.type, attrs)


def method(name=None):
    def wrapper(f):
        f.name = name if name is not None else f.__name__
        f.method = True

        argspec = getargspec(f)
        args = argspec.args
        varargs = argspec.varargs
        defaults = argspec.defaults or ()

        for arg in ("self", "receiver", "context", "m",):
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


def tryimport(modules, message=None):
    if isinstance(modules, str):
        modules = (modules,)

    for module in modules:
        try:
            return __import__(module, globals(), locals())
        except ImportError:
            pass

    if message is not None:
        warn(message)


class memoize(object):
    """Memoize the results of a function.

    Supports an optional timeout for automatic cache expiration.

    If the optional manual_flush argument is True, a function called
    "flush_cache" will be added to the wrapped function.  When
    called, it will remove all the timed out values from the cache.

    This decorator is thread safe.
    This decorator also supports class and instance methods.

    ..note:: Borrowed directly from the Wraptor library (https://pypi.python.org/pypi/Wraptor)
             With modifications inspired from https://wiki.python.org/moin/PythonDecoratorLibrary#Memoize
    """

    def __init__(self, func):
        self.func = func
        self.cache = {}
        self.lock = RLock()

    def flush(self):
        self.cache.clear()

    def __call__(self, *args):
        key = args

        if key in self.cache:
            result = self.cache[key]
        else:
            result = self.cache[key] = self.func(*args)

        return result

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self

        f = partial(self.__call__, obj)
        f.flush = self.flush
        return f


class MetaNull(type):
    """Meta Class for Null"""


class Null(type):

    __metaclass__ = MetaNull

    def __call__(self, *args, **kwargs):
        return self

Null.__class__ = Null
