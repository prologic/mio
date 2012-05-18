
import runtime
from object import Object
from utils import pymethod


class Message(Object):

    def __init__(self, name, *args, **kwargs):
        value = kwargs.get("value")
        super(Message, self).__init__(value=value)

        self.name = name
        self.args = args

        for arg in args:
            arg.parent = self

        self.terminator = self.value is None and name in ["\n", ";"]

        self._prev = None
        self._next = None
        self._parent = None

        self.create_methods()
        self["parent"] = runtime.state.find("Object")

    def __str__(self):
        messages = []

        next = self
        while next is not None:
            if next.args:
                args = "(%s)" % ", ".join([repr(arg) for arg in next.args])
            else:
                args = ""
            messages.append("%s%s" % (next.name, args))
            next = next.next

        return " ".join(messages)

    __repr__ = __str__

    @pymethod()
    def eval(self, receiver, context=None, m=None, *args):
        if context is None:
            context = receiver
        if m is None:
            m = self

        if self.terminator:
            value = context
        elif self.value is not None:
            value = self.value
        else:
            value = receiver[self.name]
            if isinstance(value, Message):
                # Prevent a recursion loop
                if value not in receiver.attrs.values():
                    value = value.eval(receiver, context, m, *self.args)
                else:
                    value = value(receiver, context, m, *self.args)
            else:
                value = value(receiver, context, m, *self.args)

        if runtime.state.stop():
            return runtime.state.returnValue
        elif runtime.state.isContinue:
            runtime.state.isContinue = False
            return runtime.state.find("None")
        elif self.next is not None:
            return self.next.eval(value, context, m)
        else:
            return receiver if self.terminator else value

    @pymethod("arg")
    def _arg(self, receiver, context, m, index):
        index = int(index.eval(context))
        return self.args[index]

    @pymethod("args")
    def _args(self, receiver, context, m):
        return self["List"].clone(self.args)

    @pymethod("next")
    def _next(self, receiver, context, m):
        return self.next or self["None"]

    @property
    def prev(self):
        return getattr(self, "_prev", None)

    @property
    def next(self):
        return getattr(self, "_next", None)

    @next.setter
    def next(self, message):
        message._prev = self
        self._next = message

    @property
    def parent(self):
        return getattr(self, "_parent", None)

    @parent.setter
    def parent(self, message):
        self._parent = message
