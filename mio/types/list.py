from mio import runtime
from mio.utils import method
from mio.object import Object


class List(Object):

    def __init__(self, value=[]):
        super(List, self).__init__(value=value)

        self.create_methods()
        self.parent = runtime.find("Object")

    def __hash__(self):
        return None

    def __len__(self):
        return len(self.value)

    def __iter__(self):
        return iter(self.value) if isinstance(self.value, list) else iter([])

    def __repr__(self):
        return repr(self.value)

    @method()
    def init(self, receiver, context, m, iterable=None):
        receiver.value = list(iterable) if iterable is not None else list()
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

    @method(property=True)
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
