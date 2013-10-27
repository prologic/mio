from time import time
from hashlib import md5
from warnings import warn
from threading import RLock
from functools import wraps
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

    def __init__(self, timeout=None, manual_flush=False):
        self.timeout = timeout
        self.manual_flush = manual_flush

        self.cache = {}
        self.cache_lock = RLock()

    def __call__(self, fn):
        def flush_cache():
            with self.cache_lock:
                for key in self.cache.keys():
                    if (time() - self.cache[key][1]) > self.timeout:
                        del(self.cache[key])

        @wraps(fn)
        def wrapped(*args, **kwargs):
            kw = kwargs.items()
            kw.sort()
            key_str = repr((args, kw))
            key = md5(key_str).hexdigest()

            with self.cache_lock:
                try:
                    result, cache_time = self.cache[key]
                    if self.timeout is not None and (time() - cache_time) > self.timeout:
                        raise KeyError
                except KeyError:
                    result, _ = self.cache[key] = (fn(*args, **kwargs), time())

            if not self.manual_flush and self.timeout is not None:
                flush_cache()

            return result

        if self.manual_flush:
            wrapped.flush_cache = flush_cache

        return wrapped


class MetaNull(type):
    """Meta Class for Null"""


class Null(type):

    __metaclass__ = MetaNull

    def __call__(self, *args, **kwargs):
        return self

Null.__class__ = Null
