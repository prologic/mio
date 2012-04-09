import re

from object import Object
from bootstrap import Lobby

class Message(Object):
    
    def __init__(self, name, line):
        self.name = name
        self.line = line

        self.args = []

        self.cached_value = None
        # Cache some messages/values
        #if re.match(r"^\d+", name):
        #    self.cached_value = Lobby["Number"].clone(int(name))
        #elif re.match(r"^\"(.*)\"$", name):
        #    m = re.match(r"^\"(.*)\"$", name)
        #    self.cached_value = Lobby["String"].clone(m.group(1))
      
        self.terminator = name in [".", "\n"]

        super(Message, self).__init__(Lobby["Message"])
    
    def __repr__(self):
        return "<Message(%r)" % self.name

    def __call__(self, receiver, context=None, *args):
        if context is None:
            context = receiver

        if self.terminator:
            value = context
        elif self.cached_value:
            value = self.cached_value
        else:
            slot = receiver[name]
            value = slot.call(receiver, context, *self.args)
      
        if self.next:
            return self.next.call(value, context)
        else:
            return value
