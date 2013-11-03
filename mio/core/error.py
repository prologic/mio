from mio import runtime
from mio.object import Object
from mio.utils import method, Null


class Error(Object):

    def __init__(self, value=Null):
        super(Error, self).__init__(value=value)

        self["type"] = None
        self["message"] = None

        self.create_methods()
        self.parent = runtime.find("Object")

    def __repr__(self):
        type = str(self["type"]) if self["type"] is not None else self.type
        message = str(self["message"]) if self["message"] is not None else ""
        return "{0:s}({1:s})".format(type, message)

    @method()
    def init(self, receiver, context, m, type=None, message=None):
        receiver["type"] = type.eval(context) if type is not None else runtime.find("String").clone("Error")
        receiver["message"] = message.eval(context) if message is not None else runtime.find("String").clone()
        return receiver
