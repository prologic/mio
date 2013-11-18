from os import path
from imp import new_module
from functools import wraps
from inspect import isfunction, isbuiltin, getmembers


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

    def __init__(self):
        super(FFI, self).__init__()

        self.module = None
        self.name = None
        self.file = None

        self.create_methods()
        self.parent = runtime.find("Object")

    def __repr__(self):
        return "FFI(name={0:s}, file={1:s})".format(repr(self.name), repr(self.file))

    def create_attributes(self):
        members = dict(getmembers(self.module))
        if "__all__" in members:
            members = dict((k, v) for k, v in members.items() if k in members["__all__"])

        for k, v in members.items():
            if isfunction(v) or isbuiltin(v):
                self[k] = wrap_function(v)
            else:
                v = runtime.state.tomio(v, Null)
                if v is not Null:
                    self[k] = v

    @method()
    def init(self, receiver, context, m, name, code):
        receiver.name = name = str(name)
        receiver.code = code = str(code)

        receiver.module = create_module(name, code)
        receiver.create_attributes()

        return receiver

    @method()
    def fromfile(self, receiver, context, m, filename):
        filename = path.abspath(path.expanduser(path.expandvars(str(filename.eval(context)))))
        name = path.splitext(path.basename(filename))[0]
        code = open(filename, "r").read()

        obj = receiver.clone()
        obj.file = filename
        obj.name = name

        obj.module = create_module(name, code)
        obj.create_attributes()

        return obj
