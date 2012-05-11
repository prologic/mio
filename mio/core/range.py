from mio import runtime
from mio.utils import method

from mio.object import Object

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
            self["start"] += self["step"]

    def __str__(self):
        if self.value is not None:
            return str(self.value)
        return super(Range, self).__str__()

    @method()
    def init(self, env, *args):
        if len(args) == 3:
            self["start"] = args[0]
            self["stop"] = args[1]
            self["step"] = args[2]
        elif len(args) == 2:
            self["start"] = args[0]
            self["stop"] = args[1]
            self["step"] = Number(1)
        elif len(args) == 1:
            self["start"] = Number(0)
            self["stop"] = args[0]
            self["step"] = Number(1)
        else:
            self["start"] = Number(0)
            self["stop"] = Number(0)
            self["step"] = Number(1)

        keys = ("start", "stop", "step")
        self.value = range(*[int(self[key]) for key in keys])
