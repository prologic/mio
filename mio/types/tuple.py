from mio import runtime
from mio.object import Object
from mio.utils import method, Null


class Tuple(Object):

    def __init__(self, value=Null):
        super(Tuple, self).__init__(value=value)

        self.create_methods()
        self.parent = runtime.find("Object")

    def __len__(self):
        return len(self.value)

    def __iter__(self):
        return iter(self.value) if isinstance(self.value, tuple) else iter(())

    def __repr__(self):
        if isinstance(self.value, tuple):
            values = ", ".join([repr(item) for item in self.value])
            return "({0:s})".format(values)
        return "()"

    @method()
    def init(self, receiver, context, m, iterable=None):
        receiver.value = tuple(iterable) if iterable is not None else tuple()
        return receiver

    # Special Methods

    @method("__getitem__")
    def getItem(self, receiver, context, m, i):
        i = int(i.eval(context))
        return receiver.value[i]

    @method("__len__")
    def getLen(self, receiver, context, m):
        return runtime.find("Number").clone(len(receiver.value))

    # General Operations

    @method()
    def count(self, receiver, context, m, value):
        return runtime.find("Number").clone(receiver.value.count(value.eval(context)))

    @method()
    def len(self, receiver, context, m):
        return runtime.find("Number").clone(len(receiver.value))

    @method()
    def at(self, receiver, context, m, index):
        return receiver.value[int(index.eval(context))]

    @method()
    def reversed(self, receiver, context, m):
        return receiver.clone(tuple(reversed(receiver.value)))

    @method()
    def sorted(self, receiver, context, m):
        return receiver.clone(tuple(sorted(receiver.value)))
