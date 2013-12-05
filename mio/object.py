from copy import copy
from operator import xor
from collections import OrderedDict
from inspect import getmembers, ismethod


from mio import runtime
from mio.utils import method, Null
from mio.errors import AttributeError, TypeError


class Object(object):

    __slots__ = ("attrs", "binding", "parent", "state", "value", "traits", "behaviors",)

    def __init__(self, value=Null, methods=True):
        super(Object, self).__init__()

        self.attrs = {}
        self.parent = None
        self.value = value

        self.traits = {}
        self.behaviors = {}

        self.binding = None

        from mio.core.state import State
        if self.__class__ is not State:
            self.state = State()

        if methods:
            self.create_methods()

    def create_methods(self):
        keys = self.__class__.__dict__.keys()
        self.attrs.update(((v.name, v) for k, v in getmembers(self, ismethod) if getattr(v, "method", False) and k in keys))

    def __hash__(self):
        return (
            reduce(xor, map(hash, self.attrs.keys()), 0) ^
            hash(self.parent) ^
            hash(self.value) ^
            reduce(xor, map(hash, self.traits.keys()), 0) ^
            reduce(xor, map(hash, self.behaviors.keys()), 0) ^
            hash(self.binding)
        )

    def __nonzero__(self):
        return bool(self.value)

    def __eq__(self, other):
        return self.value == getattr(other, "value", other)

    def __cmp__(self, other):
        return cmp(self.value, getattr(other, "value", other))

    def __contains__(self, key):
        return key in self.attrs or key in self.behaviors

    def __delitem__(self, key):
        if key in self.attrs:
            del self.attrs[key]
        elif key in self.behaviors:
            del self.behaviors[key]

    def __getitem__(self, key):
        if key in self.attrs:
            return self.attrs[key]
        elif key in self.behaviors:
            return self.behaviors[key]
        else:
            parent = self.parent
            while parent is not None:
                if key in parent:
                    return parent[key]
                parent = parent.parent

        try:
            return self.forward(key)
        except:
            raise AttributeError("{0:s} has no attribute {1:s}".format(self.type, repr(key)))

    def __setitem__(self, key, value):
        self.attrs[key] = value

    def __addtrait__(self, trait, **resolution):
        from .trait import Trait

        if not isinstance(trait, Trait):
            raise TypeError("Trait expected but got {0:s}".format(repr(getattr(trait, "type", trait.__class__.__name__))))

        for requirement in trait.requirements:
            if not self.lookup(requirement):
                raise TypeError("{0:s} requires {0:s}".format(repr(trait), repr(requirement)))

        for k, v in trait.attrs.items():
            if k in self:
                name = resolution.get(k, None)
                if not name:
                    raise TypeError("Method {0:s} of {1:s} conflicts with {2:s}".format(k, repr(trait), repr(self)))
                else:
                    self.behaviors[name] = v
            else:
                self.behaviors[k] = v

        self.traits[trait] = resolution

    def __deltrait__(self, trait):
        resolution = self.traits[trait]

        for k, v in trait.attrs.items():
            if k in self.behaviors:
                del self.behaviors[k]
            else:
                del self.behaviors[resolution[k]]

        del self.traits[trait]

    def __hastrait__(self, trait):
        if trait in self.traits:
            return True

        parent = self.parent
        while parent is not None:
            if trait in parent.traits:
                return True
            parent = parent.parent

        return False

    def __repr__(self):
        type = "{0:s}({1:s})".format(self.binding, self.type) if self.binding is not None else self.type
        default = "{0:s} at {1:s}".format(type, hex(id(self)))
        return repr(self.value) if self.value is not Null else default

    def lookup(self, name):
        try:
            self[name]
            return True
        except AttributeError:
            return False

    def clone(self, value=Null):
        obj = copy(self)

        obj.attrs = {}
        obj.parent = self
        obj.value = value if value is not Null else obj.value

        obj.traits = {}
        obj.behaviors = {}

        self.binding = None

        from mio.core.state import State
        if self.__class__ is not State:
            self.state = State()

        return obj

    def forward(self, key):
        return runtime.find(key)

    @property
    def type(self):
        return self.__class__.__name__

    # Attribute Operations

    @method("del")
    def _del(self, receiver, context, m, key):
        key = unicode(key.eval(context))
        value = receiver[key]
        del receiver[key]
        if isinstance(value, Object):
            value.bindig = None
        return runtime.find("None")

    @method()
    def has(self, receiver, context, m, key):
        key = unicode(key.eval(context))
        if key in receiver:
            return runtime.find("True")
        return runtime.find("False")

    @method()
    def set(self, receiver, context, m, key, value):
        key = unicode(key.eval(context))
        value = value.eval(context)
        if isinstance(value, Object):
            value.binding = key
        receiver[key] = value
        return value

    @method()
    def get(self, receiver, context, m, key, default=None):
        key = unicode(key.eval(context))
        default = default.eval(context) if default else runtime.find("None")
        return receiver.attrs.get(key, default)

    # Block Operations

    @method()
    def block(self, receiver, context, m, *args):
        args, body = args[:-1], args[-1:][0]

        # Evaluate kwargs first
        ctx = runtime.find("Object").clone()
        kwargs = OrderedDict([(arg.args[0].name, arg.eval(ctx)) for arg in args if arg.name == "set"])

        args = [arg for arg in args if not arg.name == "set"]

        from mio.core.block import Block
        return Block(body, args, kwargs, context)

    @method("method")
    def _method(self, receiver, context, m, *args):
        args, body = args[:-1], args[-1:][0]

        # Evaluate kwargs first
        ctx = runtime.find("Object").clone()
        kwargs = OrderedDict([(arg.args[0].name, arg.eval(ctx)) for arg in args if arg.name == "set"])

        args = [arg for arg in args if not arg.name == "set"]

        from mio.core.block import Block
        return Block(body, args, kwargs)

    # Introspection

    @method("state", True)
    def getState(self, receiver, context, m):
        return receiver.state

    @method("type", True)
    def getType(self, receiver, context, m):
        from mio.types import String
        return String(receiver.type)

    @method("parent", True)
    def _parent(self, receiver, context, m):
        if receiver.parent is not None:
            return receiver.parent
        return receiver

    @method("value", True)
    def _value(self, receiver, context, m):
        if receiver.value is not Null:
            return receiver.value
        return runtime.find("None")

    @method("__hash__", property=True)
    def hash(self, receiver, context, m):
        try:
            return runtime.find("Number").clone(hash(receiver))
        except:
            return runtime.find("None")

    @method(property=True)
    def id(self, receiver, context, m, obj=None):
        obj = obj.eval(context) if obj is not None else receiver
        return runtime.find("Number").clone(id(obj))

    @method(property=True)
    def keys(self, receiver, context, m):
        String = runtime.find("String")
        keys = [String.clone(key) for key in receiver.attrs.keys()]
        return runtime.find("List").clone(keys)

    # Object Operations

    @method()
    def init(self, receiver, context, m):
        return receiver

    @method()
    def primitive(self, receiver, context, m, method, *args):
        method = unicode(method.eval(context))
        args = [arg.eval(context).value for arg in args]
        if hasattr(receiver, method):
            return getattr(receiver, method)(*args)
        raise AttributeError("{0:s} has no attribute {1:s}".format(receiver.type, repr(method)))

    @method()
    def evalArg(self, receiver, context, m, *args):
        if len(args) > 1:
            return runtime.find("Tuple").clone(tuple(arg.eval(context) for arg in args))
        elif len(args) == 1:
            return args[0].eval(context)
        else:
            return runtime.find("None")

    @method()
    def do(self, receiver, context, m, expression):
        expression.eval(receiver)
        return receiver

    @method()
    def setParent(self, receiver, context, m, parent):
        parent = parent.eval(context)
        if parent is receiver:
            raise TypeError("Canoot set parent to self!")

        receiver.parent = parent

        return receiver

    @method()
    def setValue(self, receiver, context, m, value):
        receiver.value = value.eval(context)
        return receiver

    # Boolean Operations

    @method()
    def cmp(self, receiver, context, m, other):
        return runtime.find("Number").clone(cmp(receiver, other.eval(context)))

    # Type Conversion

    @method("__repr__")
    def getRepr(self, receiver, context, m):
        return runtime.find("String").clone(repr(receiver))

    @method("__str__")
    def getStr(self, receiver, context, m):
        return runtime.find("String").clone(unicode(receiver))
