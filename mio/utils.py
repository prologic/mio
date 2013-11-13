from warnings import warn
from inspect import getargspec, isfunction, ismethod


from mio import runtime


def default_repr(o):
    type = "{0:s}({1:s})".format(o.binding, o.type) if o.binding is not None else o.type
    return "{0:s} at {1:s}".format(type, hex(id(o)))


def format_result(result):
    if isfunction(result):
        return format_function(result)
    elif ismethod(result):
        return format_method(result)
    else:
        type = getattr(result, "type", None)
        if type is not None:
            if result.value is None:
                return

            if result["__repr__"] is not result["Object"]["__repr__"]:
                return runtime.state.eval("__repr__()", result)
            else:
                return format_object(result)
        else:
            return repr(result)


def format_value(value):
    if isfunction(value):
        return format_function(value)
    elif ismethod(value):
        return format_method(value)
    else:
        return repr(value)


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


def format_function(f):
    return getattr(f, "__doc__", "") or format_method(f)


def format_object(o):
    def format_key(k):
        return str(k).ljust(15)

    attrs = "\n".join(["  {0:s} = {1:s}".format(format_key(k), format_value(v)) for k, v in sorted(o.attrs.items())])

    return "{0:s}{1:s}".format(repr(o), ":\n{0:s}".format(attrs) if attrs else "")


def method(name=None, property=False):
    def wrapper(f):
        f.name = name if name is not None else f.__name__
        f.method = True
        f.property = property

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


class MetaNull(type):
    """Meta Class for Null"""


class Null(type):

    __metaclass__ = MetaNull

    def __call__(self, *args, **kwargs):
        return self

Null.__class__ = Null
