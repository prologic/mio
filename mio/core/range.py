from mio import runtime
from mio.utils import method

from mio.object import Object


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
        values = filter(None, [getattr(self, key, None) for key in keys])
        return "range({0:s})".format(", ".join(map(str, values)))

    @method()
    def init(self, receiver, context, m, *args):
        if len(args) == 1 and args[0].eval(context).type == "List":
            args = list(args[0].eval(context))
        else:
            args = [arg.eval(context) for arg in args]

        keys = ("start", "stop", "step")

        for i, key in enumerate(keys):
            if i < len(args):
                setattr(receiver, key, int(args[i]))
            else:
                setattr(receiver, key, None)

    @method()
    def asList(self, receiver, context, m):
        return runtime.find("List").clone(list(receiver))
