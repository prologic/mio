from mio import runtime
from mio.utils import method

from mio.object import Object


from list import List


class Map(Object):

    def __init__(self, value={}):
        super(Map, self).__init__(value=value)

        self.create_methods()
        self["parent"] = runtime.state.find("Object")

    def __iter__(self):
        for item in self.value.items():
            yield List(item)

    def __str__(self):
        pairs = ", ".join(["%s: %r" % (k, v) for k, v in self.value.items()])
        return "{%s}" % pairs

    @method()
    def init(self, receiver, context, m, *args):
        args = [arg.eval(context) for arg in args]
        it = iter(args)
        receiver.value = dict(list(zip(it, it)))

    # General Operations

    @method()
    def clear(self, receiver, context, m):
        receiver.value.clear()
        return runtime.state.find("None")

    @method()
    def copy(self, receiver, context, m):
        return self.clone(receiver.value.copy())

    @method()
    def get(self, receiver, context, m, key, default=None):
        default = default.eval(context) if default else runtime.state.find("None")
        return receiver.value.get(key.eval(context), default)

    @method()
    def has(self, receiver, context, m, key):
        key = key.eval(context)
        if key in receiver.value:
            return runtime.state.find("True")
        return runtime.state.find("False")

    @method()
    def items(self, receiver, context, m):
        items = [List(item) for item in receiver.value.items()]
        return List(items)

    @method()
    def keys(self, receiver, context, m):
        return List(receiver.value.keys())

    @method()
    def set(self, receiver, context, m, key, value):
        receiver.value[key.eval(context)] = value.eval(context)
        return receiver

    @method()
    def values(self, receiver, context, m):
        return List(receiver.value.values())
