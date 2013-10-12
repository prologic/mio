
import runtime
from object import Object
from utils import method


class Message(Object):

    def __init__(self, name, *args, **kwargs):
        value = kwargs.get("value")
        super(Message, self).__init__(value=value)

        self.name = name

        self._args = list(args)
        for arg in args:
            arg.previous = self

        self.terminator = self.value is None and name in ["\r", "\n", ";"]

        self._next = None
        self._previous = self

        self._first = self
        self._last = self

        self.create_methods()
        self.parent = runtime.state.find("Object")

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

    def eval(self, receiver, context=None, m=None, target=None):
        if context is None:
            context = receiver
        if m is None:
            m = self

        if self.terminator:
            value = context
        elif self.value is not None:
            value = self.value
        else:
            value = receiver[self.name](receiver, context, m, *self.args)

        if runtime.state.stop():
            return runtime.state.returnValue
        elif runtime.state.isContinue:
            runtime.state.isContinue = False
            return runtime.state.find("None")
        elif self.next is not None:
            return self.next.eval(value, context)
        else:
            return receiver if self.terminator else value

    @method("eval")
    def _eval(self, receiver, context, m, target=None):
        target = target.eval(context) if target is not None else context
        return receiver.eval(target)

    @method("arg")
    def evalArg(self, receiver, context, m, index):
        index = int(index.eval(context))
        if index < len(receiver.args):
            return receiver.args[index].eval(context)
        return runtime.find("None")

    @method("args")
    def getArgs(self, receiver, context, m):
        return runtime.find("List").clone(self.args)

    @method()
    def argsEvaluatedIn(self, receiver, context, m, target=None):
        target = target.eval(context) if target is not None else context
        args = [arg.eval(target) for arg in self.args]
        return runtime.find("List").clone(list(args))

    @method("first")
    def getFirst(self, receiver, context, m):
        return receiver.first

    @method("name")
    def getName(self, receiver, context, m):
        return runtime.find("String").clone(receiver.name)

    @method("next")
    def getNext(self, receiver, context, m):
        return receiver.next

    @method("last")
    def getLast(self, receiver, context, m):
        return receiver.last

    @method("previous")
    def getPrevious(self, receiver, context, m):
        return receiver.previous

    @method()
    def setArgs(self, receiver, context, m, *args):
        receiver.args = tuple(args)
        return receiver

    @method()
    def setName(self, receiver, context, m, name):
        receiver.name = name.eval(context)
        return receiver

    @method()
    def setNext(self, receiver, context, m, message):
        result = message.eval(context)
        if isinstance(result, Message):
            receiver.next = result
        else:
            receiver.next = message
        return receiver

    @property
    def args(self):
        return self._args

    @args.setter
    def args(self, args):
        self._args = list(args)
        for arg in args:
            arg.previous = self

    @property
    def first(self):
        return getattr(self, "_first", None)

    @property
    def next(self):
        return getattr(self, "_next", None)

    @next.setter
    def next(self, message):
        if self._first is None:
            self._first = self
        message._first = self._first
        message._previous = self
        self._next = message
        self._last = message

    @property
    def last(self):
        return getattr(self, "_last", None)

    @property
    def previous(self):
        return getattr(self, "_previous", None)

    @previous.setter
    def previous(self, message):
        self._previous = message
