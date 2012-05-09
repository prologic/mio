from warnings import warn
from inspect import getargspec, isfunction, ismethod


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
    attrs = {}
    for k, v in o.attrs.items():
        if ismethod(v) or isfunction(v):
            attrs[k] = format_method(v)
        else:
            attrs[k] = str(v)
    attrs = "\n".join(["  %s = %s" % (str(k).ljust(15), v)
        for k, v in sorted(attrs.items())])
    name = o.__class__.__name__
    return "%s_%s:\n%s" % (name, hex(id(o)), attrs)


def method(name=None):
    def wrapper(f):
        f.name = name or f.__name__
        f.method = True
        f.type = "mio"

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

    if message:
        warn(message)
