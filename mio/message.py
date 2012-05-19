
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
            arg.prev = self

        self.terminator = self.value is None and name in ["\n", ";"]

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
    def arg(self, receiver, context, m, index):
        index = int(index.eval(context))
        return self.args[index]

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

    @property
    def args(self):
        return tuple(self.attrs.get("args", runtime.find("List")))

    @args.setter
    def args(self, args):
        self.attrs["args"] = runtime.find("List").clone(args)

    @property
    def name(self):
        return self.attrs.get("name", runtime.find("String"))

    @name.setter
    def name(self, name):
        self.attrs["name"] = runtime.find("String").clone(name)

    @property
    def next(self):
        return self.attrs.get("next", None)

    @next.setter
    def next(self, message):
        message.prev = self
        self.attrs["next"] = message

    @property
    def prev(self):
        return self.attrs.get("prev", None)

    @prev.setter
    def prev(self, message):
        self.attrs["prev"] = message
