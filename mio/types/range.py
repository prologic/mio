from mio import runtime
from mio.utils import method

from mio.object import Object

from list import List


class Range(Object):

    def __init__(self):
        super(Range, self).__init__()

        self["start"] = runtime.find("None")
        self["stop"] = runtime.find("None")
        self["step"] = runtime.find("None")

        self.create_methods()
        self.parent = runtime.state.find("Object")

    def __iter__(self):
        start = int(self["start"])

        if self["stop"].value is None:
            stop, start = start, 0
        else:
            stop = int(self["stop"])

        step = 1 if self["step"].value is None else int(self["step"])

        if (start < stop and step > 0) or (start > stop and step < 0):
            while start < stop:
                yield start
                start += step

    def __repr__(self):
        keys = ("start", "stop", "step")
        values = filter(None, [self[key] for key in keys])
        return "range({0:s})".format(", ".join(map(str, values)))

    __str__ = __repr__

    @method()
    def init(self, receiver, context, m, *args):
        if len(args) == 1 and isinstance(args[0].eval(context), List):
            args = list(args[0].eval(context))
        else:
            args = [arg.eval(context) for arg in args]

        keys = ("start", "stop", "step")

        for i, key in enumerate(keys):
            if i < len(args):
                receiver[key] = args[i]
            else:
                receiver[key] = runtime.find("None")

    @method()
    def asList(self, receiver, context, m):
        return runtime.find("List").clone(list(receiver))
