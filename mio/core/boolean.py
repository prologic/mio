from mio import runtime
from mio.utils import Null

from mio.object import Object


class Boolean(Object):

    def __init__(self, value=Null):
        super(Boolean, self).__init__(value=value)

        self.create_methods()
        self.parent = runtime.find("Object")

    def clone(self, value=Null):
        return self
