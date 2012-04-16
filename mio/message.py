import re

from utils import method
from object import Object
from bootstrap import Lobby


class Message(Object):

    def __init__(self, name, *args):
        super(Message, self).__init__(name, proto=Lobby["Object"])

        self.name = name
        self.args = args

        self.next = None
        self.type = None
        self.value = None

        if re.match("(\d+)", self.name):
            self.type = "number"
            self.value = Lobby["Number"].clone(eval(self.name))
        elif re.match("\"(.*)\"", self.name):
            self.type = "string"
            self.value = Lobby["String"].clone(eval(self.name))

        self.terminator = name in ["\n", ";"]

    def __eq__(self, other):
        return isinstance(other, Message) and other.name == self.name

    def __add__(self, message):
        self.next = message
        return message

    def __repr__(self):
        messages = []

        next = self
        while next is not None:
            messages.append(next.name)
            if next.args:
                args = ", ".join([repr(arg) for arg in next.args])
                messages.append("(%s)" % args)
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

        if self.next:
            return self.next(value, context)
        else:
            return value

    def pprint(self):
        next = self
        messages = []
        while next is not None:
            messages.append(repr(next))
            next = next.next

        return "\n".join(["%s%s" % (" " * i, x)
            for i, x in enumerate(messages)])

    @method("call")
    def _call(self, receiver, context, *args):
        return self(reciver, context, *args)
