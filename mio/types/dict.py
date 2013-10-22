from copy import copy


from mio import runtime
from mio.utils import method

from mio.object import Object


class Dict(Object):

    def __init__(self, value={}):
        super(Dict, self).__init__(value=value)

        self.create_methods()
        self.parent = runtime.state.find("Object")

    def __iter__(self):
        return iter(self.value) if isinstance(self.value, dict) else iter({})

    def __repr__(self):
        items = ", ".join(["{0:s}={1:s}".format(repr(k), repr(v)) for k, v in self.value.items()])
        return "dict({0:s})".format(items)

    @method()
    def init(self, receiver, context, m, d=None):
        receiver.value = copy(d.eval(context).value) if d is not None else dict()

    # General Operations

    @method()
    def get(self, receiver, context, m, key):
        return receiver.value[key.eval(context)]

    @method()
    def set(self, receiver, context, m, key, value):
        receiver.value[key.eval(context)] = value.eval(context)
        return receiver

    @method()
    def keys(self, receiver, context, m):
        return runtime.find("List").clone(receiver.value.keys())

    @method()
    def values(self, receiver, context, m):
        return runtime.find("List").clone(receiver.value.values())

    @method()
    def len(self, receiver, context, m):
        return runtime.find("Number").clone(len(receiver.value))
