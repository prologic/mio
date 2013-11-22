from copy import copy


from mio import runtime
from mio.utils import method
from mio.object import Object
from mio.errors import StopIteration


class Generator(Object):

    def __init__(self):
        super(Generator, self).__init__()

        self.context = None
        self.message = None

        self.create_methods()
        self.parent = runtime.find("Object")

    @method("init")
    def init(self, receiver, context, m):
        receiver.context = copy(context["call"]["sender"])
        receiver.message = context["call"]["sender"]["call"]["message"]
        return receiver

    @method("__next__")
    def getNext(self, receiver, context, m):
        if receiver.message.terminator:
            raise StopIteration()
        try:
            return receiver.message.eval(receiver.context)
        finally:
            next = receiver.message
            while next.next is not None:
                if next.terminator:
                    next = next.next
                    break
                next = next.next
            receiver.message = next
