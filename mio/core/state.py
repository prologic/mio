from mio import runtime
from mio.object import Object
from mio.utils import method, Null


class State(Object):

    def __init__(self):
        super(State, self).__init__()

        self.isContinue = False
        self.isReturn = False
        self.isBreak = False

        self.create_methods()
        self.parent = runtime.find("Object")

    def __repr__(self):
        if self.isContinue:
            type = "Continue"
        elif self.isReturn:
            type = "Return"
        elif self.isBreak:
            type = "Break"
        else:
            type = "Normal"

        value = str(self.value) if self.value is not Null else ""

        return "{0:s}State({1:s})".format(type, value)

    def reset(self):
        keys = ("isContinue", "isReturn", "isBreak",)
        for key in keys:
            setattr(self, key, False)

    @property
    def stop(self):
        keys = ("isContinue", "isReturn", "isBreak",)
        return any((getattr(self, key) for key in keys))

    @method("stop")
    def _stop(self, receiver, context, m):
        return runtime.find("True") if receiver.stop else runtime.find("False")

    @method()
    def setContinue(self, receiver, context, m, value=None):
        if context.type != "Locals":
            return receiver

        value = bool(value.eval(context)) if value is not None else True
        receiver.isContinue = value
        return receiver

    @method()
    def setReturn(self, receiver, context, m, value=None):
        if context.type != "Locals":
            return receiver

        value = value.eval(context) if value is not None else Null
        receiver.isReturn = True
        receiver.value = value
        return receiver

    @method()
    def setBreak(self, receiver, context, m, value=None):
        if context.type != "Locals":
            return receiver

        value = bool(value.eval(context)) if value is not None else True
        receiver.isBreak = value
        return receiver
