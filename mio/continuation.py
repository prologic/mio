from copy import copy

import runtime
from object import Object
from utils import pymethod, Null


class Continuation(Object):

    def __init__(self, value=Null):
        super(Continuation, self).__init__(value=value)

        self.context = None
        self.message = None

        self.create_methods()
        self["parent"] = runtime.state.find("Object")

    @pymethod("call")
    def call(self, receiver, context, m):
        return receiver.message.eval(receiver.context)

    @pymethod("current")
    def current(self, receiver, context, m):
        continuation = receiver.clone()
        continuation.context = copy(context)
        continuation.message = m.previous.previous
        return continuation
