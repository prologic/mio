from mio import runtime
from mio.utils import method
from mio.object import Object
from mio.errors import IndexError


class Range(Object):

    def __init__(self):
        super(Range, self).__init__()

        self.start = None
        self.stop = None
        self.step = None

        self.create_methods()
        self.parent = runtime.find("Object")

    def __iter__(self):
        start = self.start

        if self.stop is None:
            stop, start = start, 0
        else:
            stop = self.stop

        step = 1 if self.step is None else self.step

        if (start < stop and step > 0) or (start > stop and step < 0):
            while start < stop:
                yield runtime.find("Number").clone(start)
                start += step

    def __repr__(self):
        keys = ("start", "stop", "step")
        values = [x for x in [getattr(self, key, None) for key in keys] if x is not None]
        return "range({0:s})".format(", ".join(map(str, values)))

    @method()
    def init(self, receiver, context, m, *args):
        keys = ("start", "stop", "step")

        for i, key in enumerate(keys):
            if i < len(args):
                setattr(receiver, key, int(args[i]))
            else:
                setattr(receiver, key, None)

    @method()
    def setStep(self, receiver, context, m, value):
        receiver.step = int(value.eval(context))
        return receiver

    @method("__getitem__")
    def getItem(self, receiver, context, m, i):
        i = int(i.eval(context))

        start = receiver.start

        if receiver.stop is None:
            stop, start = start, 0
        else:
            stop = receiver.stop

        step = 1 if receiver.step is None else receiver.step

        if (start < stop and step > 0) or (start > stop and step < 0):
            length = ((stop - start) / step) + (stop % step)
        else:
            length = 0

        if i > length:
            raise IndexError("range index out of range")

        value = start + (step * i)

        return runtime.find("Number").clone(value)

    @method("__len__")
    def mio__len__(self, receiver, context, m):
        start = receiver.start

        if receiver.stop is None:
            stop, start = start, 0
        else:
            stop = receiver.stop

        step = 1 if receiver.step is None else receiver.step

        if (start < stop and step > 0) or (start > stop and step < 0):
            length = ((stop - start) / step) + (stop % step)
        else:
            length = 0

        return runtime.find("Number").clone(length)
