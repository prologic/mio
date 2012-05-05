from object import Object
from pymethod import pymethod
from utils import method, Null


class Call(Object):

    def __init__(self, value=Null, parent=None):
        super(Call, self).__init__(value=value, parent=parent)


class Method(Object):

    def __init__(self, context, name, args, message, parent=None):
        super(Method, self).__init__(parent=parent)

        self.context = context
        self.name = name
        self.args = args
        self.message = message

        self.locals = self.context.clone(type=self["String"].clone("Locals"))

    def __repr__(self):
        args = ",".join([arg.name for arg in self.args]) if self.args else ""
        return "%s(%s)" % (self.name, args)

    def __call__(self, receiver, context, m, *args):
        locals = self.locals

        call = Call(parent=self["Object"])

        call["message"] = m
        call["sender"] = context
        call["target"] = receiver
        call["context"] = self.context

        locals["call"] = call
        locals["self"] = receiver
        locals["args"] = self["List"].clone(args)

        for i, arg in enumerate(self.args):
            if i < len(args):
                locals[arg.name] = args[i](context)
            else:
                locals[arg.name] = self["None"](context)

        try:
            self["state"].reset()
            return self.message(locals)
        finally:
            self["state"].reset()

    @method()
    def call(self, receiver, context, m, *args):
        return self(receiver, context, m, *args)

    @pymethod()
    def code(self):
        return self["String"].clone(repr(self.message))
