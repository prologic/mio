from mio import runtime
from mio.object import Object
from mio.errors import TypeError


class Trait(Object):

    def __init__(self):
        super(Trait, self).__init__()

        self.create_methods()
        self.parent = runtime.find("Trait" if self.__class__ is not Trait else "Object")

    def __setitem__(self, key, value):
        if getattr(value, "type", None) != "Block":
            raise TypeError("Traits cannot contain state!")
        super(Trait, self).__setitem__(key, value)
