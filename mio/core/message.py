from inspect import ismethod


from mio import runtime
from mio.utils import method
from mio.object import Object
from mio.errors import Error, AttributeError, TypeError


class Message(Object):

    def __init__(self, name=None, value=None, args=None):
        super(Message, self).__init__(value=value)

        self.name = name
        self.value = value
        self.args = args if args is not None else []

        self.call = args is not None
        self.terminator = self.value is None and name in ["\r", "\n", ";"]

        self._previous = self
        self._first = self
        self._last = self
        self._next = None

        self.create_methods()
        self.parent = runtime.find("Object")

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

    def eval(self, receiver, context=None, m=None, target=None):
        context = receiver if context is None else context
        m = self if m is None else m

        try:
            while m is not None:
                if m.terminator:
                    value = context
                elif m.value is not None:
                    runtime.state.value = value = m.value
                else:
                    if isinstance(receiver, Object):
                        obj = receiver[m.name]

                        if isinstance(obj, Object) and obj.type in ("Error", "Object"):
                            if m.call:
                                try:
                                    receiver = obj
                                    obj = obj["__call__"]
                                except AttributeError:
                                    raise TypeError("{0} is not callable".format(obj))

                            else:
                                if "__get__" in obj:
                                    receiver = obj
                                    obj = obj["__get__"]
                                    m.call = True

                        if callable(obj) and (m.call or getattr(obj, "property", False)):
                            # XXX: New way...
                            if ismethod(obj) and obj.name not in ("block", "method",):
                                if m.args and m.args[0].name == "*" and m.args[0].args:
                                    args = tuple(m.args[0].eval(context))
                                else:
                                    args = m.args
                            elif isinstance(obj, Object):
                                if m.args and m.args[0].name == "*":
                                    args = tuple(m.args[0].eval(context))
                                else:
                                    args = m.args
                            else:
                                args = m.args
                            runtime.state.value = value = obj(receiver, context, m, *args)
                        else:
                            runtime.state.value = value = obj
                    else:
                        runtime.state.value = value = receiver

                if context.state.stop:
                    return context.state.value

                receiver = value
                m = m.next
        except Error as e:
            e.stack.insert(0, m)
            raise

        try:
            returnValue = runtime.state.value if runtime.state.value is not None else receiver
            runtime.find("Root")["_"] = returnValue
            return returnValue
        finally:
            runtime.state.value = None

    @method()
    def init(self, receiver, context, m):
        receiver._previous = receiver
        receiver._first = receiver
        receiver._last = receiver
        receiver._next = None

    @method("eval")
    def _eval(self, receiver, context, m, target=None):
        target = target.eval(context) if target is not None else context
        return receiver.eval(target)

    @method("arg")
    def evalArg(self, receiver, context, m, index, target=None):
        index = int(index.eval(context))
        target = target.eval(context) if target is not None else context
        if index < len(receiver.args):
            return receiver.args[index].eval(target)
        return runtime.find("None")

    @method("args", True)
    def getArgs(self, receiver, context, m):
        return runtime.find("List").clone(receiver.args)

    @method()
    def evalArgs(self, receiver, context, m, target=None):
        target = target.eval(context) if target is not None else context
        args = [arg.eval(target, context) for arg in receiver.args]
        return runtime.find("List").clone(list(args))

    @method("first", True)
    def getFirst(self, receiver, context, m):
        return receiver.first

    @method("name", True)
    def getName(self, receiver, context, m):
        return runtime.find("String").clone(receiver.name)

    @method("next", True)
    def getNext(self, receiver, context, m):
        return receiver.next

    @method("last", True)
    def getLast(self, receiver, context, m):
        return receiver.last

    @method("previous", True)
    def getPrevious(self, receiver, context, m):
        return receiver.previous

    @method()
    def setArgs(self, receiver, context, m, *args):
        receiver.args = args
        receiver.call = True
        return receiver

    @method()
    def setName(self, receiver, context, m, name):
        receiver.name = name.eval(context)
        return receiver

    @method()
    def setNext(self, receiver, context, m, message):
        receiver.next = message.eval(context)
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
        message._first = self._first
        message._previous = self

        self._next = message

        next = self._first
        while next is not None:
            next._last = message
            next = next._next

    @property
    def last(self):
        return getattr(self, "_last", None)

    @property
    def previous(self):
        return getattr(self, "_previous", None)

    @previous.setter
    def previous(self, message):
        self._previous = message
