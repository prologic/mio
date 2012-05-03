from mio.utils import Null
from mio.object import Object
from mio.pymethod import pymethod


class Range(Object):

    def __init__(self, value=Null, parent=None):
        super(Range, self).__init__(value=value, parent=parent)

        self["start"] = self["Number"].clone(0)
        self["stop"] = self["Number"].clone(0)
        self["step"] = self["Number"].clone(1)

    def __iter__(self):
        while self["start"] < self["stop"]:
            yield self["start"]
            self["start"] = self["Number"].clone(self["start"] + self["step"])

    def __repr__(self):
        if self.value is not Null:
            return repr(self.value)
        return super(Range, self).__repr__()

    __str__ = __repr__

    @pymethod()
    def init(self, *args):
        if len(args) == 3:
            self["start"] = args[0]
            self["stop"] = args[1]
            self["step"] = args[2]
        elif len(args) == 2:
            self["start"] = args[0]
            self["stop"] = args[1]
            self["step"] = self["Number"].clone(1)
        elif len(args) == 1:
            self["start"] = self["Number"].clone(0)
            self["stop"] = args[0]
            self["step"] = self["Number"].clone(1)
        else:
            self["start"] = self["Number"].clone(0)
            self["stop"] = self["Number"].clone(0)
            self["step"] = self["Number"].clone(1)

        keys = ("start", "stop", "step")
        self.value = range(*[int(self[key]) for key in keys])
