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

    @method()
    def setNextMessage(self, receiver, context, m, message):
        receiver.message = message.eval(context).next
        return receiver

    @method("__next__")
    def getNext(self, receiver, context, m):
        if receiver.message is None:
            raise StopIteration()
        return receiver.message.eval(receiver.context)
