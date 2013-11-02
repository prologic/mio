from copy import copy


from mio import runtime
from mio.object import Object
from mio.utils import method, Null


class List(Object):

    def __init__(self, value=Null):
        super(List, self).__init__(value=value)

        self.create_methods()
        self.parent = runtime.find("Object")

    def __len__(self):
        return len(self.value)

    def __iter__(self):
        return iter(self.value) if isinstance(self.value, list) else iter([])

    def __repr__(self):
        if isinstance(self.value, list):
            values = ", ".join([repr(item) for item in self.value])
            return "list({0:s})".format(values)
        return "List"

    @method()
    def init(self, receiver, context, m, l=None):
        receiver.value = copy(l.eval(context).value) if l is not None else list()

    # Special Methods

    @method("__getitem__")
    def mio__getitem__(self, receiver, context, m, i):
        i = int(i.eval(context))
        return receiver.value[i]

    @method("__len__")
    def mio__len__(self, receiver, context, m):
        return runtime.find("Number").clone(len(receiver.value))

    # General Operations

    @method()
    def append(self, receiver, context, m, item):
        receiver.value.append(item.eval(context))
        return receiver

    @method()
    def insert(self, receiver, context, m, index, value):
        receiver.value.insert(int(index.eval(context)), value.eval(context))
        return receiver

    @method()
    def count(self, receiver, context, m, value):
        return runtime.find("Number").clone(receiver.value.count(value.eval(context)))

    @method()
    def extend(self, receiver, context, m, *args):
        args = [arg.eval(context) for arg in args]
        receiver.value.extend(args)
        return receiver

    @method()
    def len(self, receiver, context, m):
        return runtime.find("Number").clone(len(receiver.value))

    @method()
    def at(self, receiver, context, m, index):
        return receiver.value[int(index.eval(context))]

    @method()
    def reverse(self, receiver, context, m):
        receiver.value.reverse()
        return receiver

    @method()
    def reversed(self, receiver, context, m):
        return receiver.clone(list(reversed(receiver.value)))

    @method()
    def sort(self, receiver, context, m):
        receiver.value.sort()
        return receiver

    @method()
    def sorted(self, receiver, context, m):
        return receiver.clone(list(sorted(receiver.value)))
