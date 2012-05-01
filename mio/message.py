import re
from decimal import Decimal

from utils import method
from object import Object
from bootstrap import Lobby


class Message(Object):

    def __init__(self, name, *args):
        super(Message, self).__init__(name, parent=Lobby["Object"])

        self.name = name
        self.args = args

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

    def __repr__(self):
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

    def __call__(self, receiver, context=None, *args):
        if context is None:
            context = receiver

        if self.terminator:
            value = context
        elif self.value:
            value = self.value
        else:
            slot = receiver[self.name]
            value = slot(receiver, context, *self.args)

        if self["state"].stop():
            return self["state"]["return"]
        elif self.next:
            return self.next(value, context)
        else:
            return value

    @method("call")
    def _call(self, receiver, context, *args):
        return self(receiver, context, *args)

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
