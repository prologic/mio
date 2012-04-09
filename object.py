from errors import SlotError

class Object(object):

    __slots__ = ("slots", "protos", "value",)

    def __init__(self, proto=None, value=None):
        super(Object, self).__init__()

        self.protos = proto or ()
        self.value = value

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
        return Object(self, value)

    def __repr__(self):
        return repr(self.value)

    def __call__(self):
        return self
