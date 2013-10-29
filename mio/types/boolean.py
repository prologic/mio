from mio import runtime
from mio.object import Object


class Boolean(Object):

    def __init__(self, value=None):
        super(Boolean, self).__init__(value=value)

        self.create_methods()
        self.parent = runtime.find("Object")
