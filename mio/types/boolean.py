from mio import runtime
from mio.utils import method, Null

from mio.object import Object


class Boolean(Object):

    def __init__(self, value=None):
        super(Boolean, self).__init__(value=value)

        self.create_methods()
        self.parent = runtime.state.find("Object")

    def clone(self, value=Null):
        return self

    def __repr__(self):
        return repr(self.value)

    __str__ = __repr__
