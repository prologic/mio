import re
from decimal import Decimal

import runtime
from utils import method
from object import Object

from mio.core import Number
from mio.core import String


class Message(Object):

    def __init__(self, name, *args):
        super(Message, self).__init__()

        self["parent"] = runtime.state.find("Object")

        self.name = name
        self.args = args

        for arg in args:
            arg.parent = self

        if isinstance(self.name, Decimal):
            self.type = "Number"
            self.value = Number(self.name)
        elif re.match("\"(.*)\"", self.name):
            self.type = "String"
            self.value = String(eval(self.name))
        else:
            self.type = None
            self.value = None

        self.terminator = name in ["\n", ";"]

        self._prev = None
        self._next = None
        self._parent = None

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

    @method()
    def eval(self, receiver, context=None, m=None, *args):
        #import pudb; pudb.set_trace()

        if context is None:
            context = receiver
        if m is None:
            m = self

        if self.terminator:
            value = context
        elif self.value:
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
        elif self.next:
            return self.next.eval(value, context, m)
        else:
            return receiver if self.terminator else value

    @method()
    def args(self):
        return self["List"].clone(self.args)

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
