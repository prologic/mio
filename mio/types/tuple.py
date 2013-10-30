from copy import copy


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
            return "tuple({0:s})".format(values)
        return "Tuple"

    @method()
    def init(self, receiver, context, m, l=None):
        receiver.value = copy(l.eval(context).value) if l is not None else tuple()

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
