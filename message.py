import re

from object import Object
from bootstrap import Lobby

class Message(Object):
    
    def __init__(self, name, *args):
        self.name = name
        self.args = args

        self.next = None

        if re.match("(\d+)", self.name):
            self.cached_value = Lobby["Number"].clone(eval(self.name))
        elif re.match("\"(.*)\"", self.name):
            self.cached_value = Lobby["String"].clone(eval(self.name))
        else:
            self.cached_value = None

        self.terminator = name in ["\n", ";"]

        super(Message, self).__init__(Lobby["Message"])

    def __add__(self, message):
        self.next = message
        return message
    
    def __repr__(self):
        args = repr(self.args) if self.args else ""
        return "<Message[%s%s]>" % (self.name, args)

    def __call__(self, receiver, context=None, *args):
        if context is None:
            context = receiver

        if self.terminator:
            value = context
        elif self.cached_value:
            value = self.cached_value
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
