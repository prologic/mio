from mio import runtime
from mio.object import Object
from mio.utils import method, Null


class Module(Object):

    def __init__(self, value=Null):
        super(Module, self).__init__(value=value)

        self["__file__"] = runtime.find("None")
        self["__name__"] = runtime.find("None")

        self.create_methods()
        self.parent = runtime.find("Object")

    def __repr__(self):
        return "Module(__name__={0:s}, __file__={1:s})".format(repr(self["__name__"]), repr(self["__file__"]))

    @method()
    def init(self, receiver, context, m, name, file):
        name = name.eval(context)
        file = file.eval(context)

        receiver["__name__"] = name
        receiver["__file__"] = file

        runtime.state.load(str(file), receiver, receiver)

        return receiver
