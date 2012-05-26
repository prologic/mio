from mio import runtime
from mio.utils import pymethod, Null

from mio.object import Object


class Boolean(Object):

    def __init__(self, value=None):
        super(Boolean, self).__init__(value=bool(value))

        self.create_methods()
        self["parent"] = runtime.state.find("Object")

    def clone(self, value=Null):
        if value is not Null:
            value = bool(value)
        return super(Boolean, self).clone(value)

    def __repr__(self):
        return repr(self.value)

    __str__ = __repr__

    @pymethod()
    def init(self, receiver, context, m, value=None):
        if value is not None:
            value = bool(value.eval(context))
        else:
            value = runtime.find("None").clone()

        receiver.value = value
