import re
from decimal import Decimal

from utils import method
from object import Object
from bootstrap import Lobby
from pymethod import pymethod


class Message(Object):

    def __init__(self, name, *args):
        super(Message, self).__init__(name, parent=Lobby["Object"])

        self.name = name
        self.args = args

        for arg in args:
            arg.parent = self

        self.type = None
        self.value = None

        if isinstance(self.name, Decimal):
            self.type = "number"
            self.value = Lobby["Number"].clone(self.name)
        elif re.match("\"(.*)\"", self.name):
            self.type = "string"
            self.value = Lobby["String"].clone(eval(self.name))

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

    def __call__(self, receiver, context=None, m=None, *args):
        if context is None:
            context = receiver
        if m is None:
            m = self

        if self.terminator:
            value = context
        elif self.value:
            value = self.value
        else:
            slot = receiver[self.name]
            value = slot(receiver, context, m, *self.args)

        if self["state"].stop():
            return self["state"]["return"]
        elif self["state"]["isContinue"].value:
            self["state"]["isContinue"] = self["False"]
            return self["None"]
        elif self.next:
            return self.next(value, context, m)
        else:
            return receiver if self.terminator else value

    @pymethod()
    def args(self):
        return self["List"].clone(self.args)

    @method("call")
    def _call(self, receiver, context, m, *args):
        return self(receiver, context, m, *args)

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
