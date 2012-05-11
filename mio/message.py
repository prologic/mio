import re
from decimal import Decimal

import runtime
from utils import method
from object import Object

from mio.core import Number
from mio.core import String


class Message(Object):

    def __init__(self, name, *args):
        super(Message, self).__init__()

        self.name = name
        self.args = args

        for arg in args:
            arg.parent = self

        if isinstance(self.name, Decimal):
            self.type = "Number"
            self.value = Number(self.name)
        elif re.match("\"(.*)\"", self.name):
            self.type = "String"
            self.value = String(eval(self.name))
        else:
            self.type = None
            self.value = None

        self.terminator = name in ["\n", ";"]

        self._prev = None
        self._next = None
        self._parent = None

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

    def perform_on(self, env, locals, target=None):
        target = target or env.target

        m = self
        result = target

        while m is not None:
            if m.value is not None:
                result = m.value
            else:
                result = target.perform(env.update({
                    "msg": m,
                    "sender": locals,
                    "target": target
                }))
            target = result
            m = m.next
        return result

    def eval_arg(self, env, i):
        if not i < len(self.args):
            return runtime.state.find("None")
        msg = self.args[i]
        if msg.value is not None and msg.next is None:
            return msg.value
        return msg.perform_on(env.update({"msg": msg}), env.sender, env.sender)

    def eval_args(self, env):
        return [self.eval_arg(env, i) for i, arg in enumerate(self.args)]

    @method("arg")
    def _arg(self, env, index):
        index = int(index.eval(context))
        return self.args[index]

    @method("args")
    def _args(self, env):
        return self["List"].clone(self.args)

    @method("next")
    def _next(self, env):
        return self.next or self["None"]

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

    @property
    def parent(self):
        return getattr(self, "_parent", None)

    @parent.setter
    def parent(self, message):
        self._parent = message
