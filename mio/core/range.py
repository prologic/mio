from mio import runtime
from mio.utils import pymethod

from mio.object import Object

from list import List
from number import Number


class Range(Object):

    def __init__(self, value=range(0)):
        super(Range, self).__init__(value=value)

        self["start"] = Number(0)
        self["stop"] = Number(0)
        self["step"] = Number(1)

        self.create_methods()
        self["parent"] = runtime.state.find("Object")

    def __iter__(self):
        while self["start"] < self["stop"]:
            yield self["start"]
            self["start"] = self["start"].clone(self["start"] + self["step"])

    @pymethod()
    def init(self, receiver, context, m, *args):
        if len(args) == 1 and isinstance(args[0].eval(context), List):
            args = list(args[0].eval(context))
        else:
            args = [arg.eval(context) for arg in args]

        ints = [int(arg) for arg in args]
        keys = ("start", "stop", "step")

        for i, key in enumerate(keys):
            if i < len(args):
                receiver[key] = args[i]
            else:
                receiver[key] = runtime.find("None")

        if receiver["stop"] == None:
            receiver["start"], receiver["stop"] = Number(0), receiver["start"]

        if receiver["step"] == None:
            receiver["step"] = Number(1)

        receiver.value = range(*ints)
