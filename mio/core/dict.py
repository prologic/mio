from mio import runtime
from mio.utils import pymethod

from mio.object import Object


from list import List
from number import Number


class Dict(Object):

    def __init__(self, value={}):
        super(Dict, self).__init__(value=value)

        self.create_methods()
        self["parent"] = runtime.state.find("Object")

    def __iter__(self):
        for item in self.value.items():
            yield List(item)

    def __repr__(self):
        values = ", ".join(["%r, %r" % (k, v) for k, v in self.value.items()])
        return "dict(%s)" % values

    __str__ = __repr__

    @pymethod()
    def init(self, receiver, context, m, iterable=None):
        iterable = iterable.eval(context) if iterable is not None else List()
        if not isinstance(iterable, List):
            raise TypeError("%s object is not iterable" % iterable.type)
        iterable = iter(iterable)
        receiver.value = dict(list(zip(iterable, iterable)))

    # General Operations

    @pymethod()
    def clear(self, receiver, context, m):
        receiver.value.clear()
        return runtime.state.find("None")

    @pymethod()
    def copy(self, receiver, context, m):
        return receiver.clone(receiver.value.copy())

    @pymethod()
    def len(self, receiver, context, m):
        return Number(len(receiver.value))

    @pymethod()
    def get(self, receiver, context, m, key, default=None):
        if default is not None:
            default = default.eval(context)
        else:
            default = runtime.state.find("None")

        return receiver.value.get(key.eval(context), default)

    @pymethod()
    def has(self, receiver, context, m, key):
        key = key.eval(context)
        if key in receiver.value:
            return runtime.state.find("True")
        return runtime.state.find("False")

    @pymethod()
    def items(self, receiver, context, m):
        items = [List(item) for item in receiver.value.items()]
        return List(items)

    @pymethod()
    def keys(self, receiver, context, m):
        return List(receiver.value.keys())

    @pymethod()
    def set(self, receiver, context, m, key, value):
        receiver.value[key.eval(context)] = value.eval(context)
        return receiver

    @pymethod()
    def values(self, receiver, context, m):
        return List(receiver.value.values())
