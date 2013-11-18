from posix import listdir
from posixpath import dirname, splitext
from inspect import getmembers, getmodule, isclass


from mio import runtime
from mio.object import Object


def load_objects():
    for filename in listdir(dirname(__file__)):
        name, ext = splitext(filename)
        if ext == ".py" and name != "__init__":
            module = __import__("mio.types.{0:s}".format(name), fromlist=["mio.types"])
            predicate = lambda x: isclass(x) and issubclass(x, Object) and getmodule(x) is module and x is not Types
            for name, object in getmembers(module, predicate):
                globals()[name] = object
                yield name, object


class Types(Object):

    def __init__(self):
        super(Types, self).__init__()

        self.create_objects()

        self.create_methods()
        self.parent = runtime.find("Object")

    def create_objects(self):
        for name, object in objects:
            self[name] = object()


objects = list(load_objects())


#__all__ = tuple(map(itemgetter(0), objects))
