from os import listdir, path
from inspect import getmembers, getmodule, isclass


from mio import runtime
from mio.utils import Null
from mio.object import Object


class Types(Object):

    def __init__(self, value=Null):
        super(Types, self).__init__(value=value)

        self.create_objects()

        self.create_methods()
        self.parent = runtime.find("Object")

    def __repr__(self):
        return "Types"

    def load_objects(self):
        for filename in listdir(path.dirname(__file__)):
            name, ext = path.splitext(filename)
            if ext == ".py" and name != "__init__":
                module = __import__("mio.types.{0:s}".format(name), fromlist=["mio.types"])
                predicate = lambda x: isclass(x) and issubclass(x, Object) and getmodule(x) is module and x is not Types
                for name, object in getmembers(module, predicate):
                    yield name, object

    def create_objects(self):
        for name, object in self.load_objects():
            self[name] = object()
