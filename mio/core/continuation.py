from copy import copy


from mio import runtime
from mio.utils import method, Null
from mio.object import Object


class Continuation(Object):

    def __init__(self, value=Null):
        super(Continuation, self).__init__(value=value)

        self.context = None
        self.message = None

        self.create_methods()
        self.parent = runtime.find("Object")

    def __call__(self, receiver, context, m):
        if not m.call:
            return self
        return self.message.eval(self.context)

    @method("current", True)
    def current(self, receiver, context, m):
        continuation = receiver.clone()
        continuation.context = copy(context)
        continuation.message = m.previous.previous
        return continuation
