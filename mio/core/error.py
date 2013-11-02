from mio import runtime
from mio.object import Object
from mio.utils import method, Null


class Error(Object):

    def __init__(self, value=Null):
        super(Error, self).__init__(value=value)

        self["message"] = None
        self["error"] = None

        self.create_methods()
        self.parent = runtime.find("Object")

    def __repr__(self):
        error = str(self["error"]) if self["error"] is not None else self.type
        message = str(self["message"]) if self["message"] is not None else ""
        return "{0:s}({1:s})".format(error, message)

    @method()
    def init(self, receiver, context, m, error=None, message=None):
        if error is not None:
            receiver["error"] = error.eval(context)
        if message is not None:
            receiver["message"] = message.eval(context)
        return receiver
