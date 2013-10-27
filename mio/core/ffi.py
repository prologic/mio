from os import path
from imp import new_module
from functools import wraps
from inspect import isfunction, isbuiltin, getmembers


from funcy import compose, project


from mio import runtime
from mio.object import Object
from mio.utils import method, Null


def create_module(name, code):
    module = new_module(name)
    exec(compile(code, "String", "exec"), module.__dict__)
    return module


def wrap_function(f):
    @wraps(f)
    def wrapper(receiver, context, m, *args, **kwargs):
        args = tuple(runtime.state.frommio(arg.eval(context)) for arg in args)
        kwargs = dict((k, runtime.state.frommio(v.eval(context))) for k, v in kwargs.items())
        return runtime.state.tomio(f(*args, **kwargs))
    return wrapper


class FFI(Object):

    def __init__(self, value=Null):
        super(FFI, self).__init__(value=value)

        self.module = None
        self["__name__"] = runtime.find("None")
        self["__file__"] = runtime.find("None")

        self.create_methods()
        self.parent = runtime.find("Object")

    def __repr__(self):
        return "FFI(__name__={0:s}, __file__={1:s})".format(repr(self["__name__"]), repr(self["__file__"]))

    def create_attributes(self):
        members = dict(getmembers(self.module))
        if "__all__" in members:
            members = project(members, members["__all__"])

        for k, v in members.items():
            if isfunction(v) or isbuiltin(v):
                self[k] = wrap_function(v)
            else:
                v = runtime.state.tomio(v, Null)
                if v is not Null:
                    self[k] = v

    @method()
    def init(self, receiver, context, m, name, code):
        name = name.eval(context)
        code = code.eval(context)

        receiver.module = create_module(str(name), str(code))
        receiver.create_attributes()

        return receiver

    @method()
    def fromfile(self, receiver, context, m, filename):
        filename = compose(path.abspath, path.expanduser, path.expandvars)(str(filename.eval(context)))
        name = path.splitext(path.basename(filename))[0]
        code = open(filename, "r").read()

        obj = receiver.clone()
        obj["__file__"] = runtime.find("String").clone(filename)

        obj.module = create_module(name, code)
        obj.create_attributes()

        return obj
