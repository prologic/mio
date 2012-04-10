from copy import copy

from errors import SlotError

class Object(object):

    __slots__ = ("slots", "protos", "value",)

    def __init__(self, value=None, proto=None):
        super(Object, self).__init__()

        self.value = value

        self.protos = (proto,) if proto is not None else ()

        self.slots = {}
    
    def __getitem__(self, name):
        if name in self.slots:
            return self.slots[name]

        message = None

        for proto in self.protos:
            message = proto[name]

        if message:
            return message
        else:
            raise SlotError(name)

    def __setitem__(self, name, message):
        self.slots[name] = message
    
    def clone(self, value=None):
        return Object(value if value is not None else copy(self.value),
                proto=self)

    def __repr__(self):
        if self.value is not None:
            return repr(self.value)
        else:
            slots = "\n".join([" %s = %s" % (k, v)
                for k, v in self.slots.items()])
            return "Object_%s:\n%s" % (id(self), slots)

    def __call__(self, *args, **kwargs):
        return self
