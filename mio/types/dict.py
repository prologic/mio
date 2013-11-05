from copy import copy


from mio import runtime
from mio.object import Object
from mio.utils import method, Null


class Dict(Object):

    def __init__(self, value={}):
        super(Dict, self).__init__(value=value)

        self.create_methods()
        self.parent = runtime.find("Object")

    def __iter__(self):
        return iter(self.value) if isinstance(self.value, dict) else iter({})

    def __repr__(self):
        if isinstance(self.value, dict):
            items = ", ".join(["{0:s}={1:s}".format(repr(k), repr(v)) for k, v in self.value.items()])
            return "dict({0:s})".format(items)
        return "Dict"

    @method()
    def init(self, receiver, context, m, *args):
        ctx = runtime.find("Object").clone()
        if len(args) == 1 and args[0].eval(ctx).type == "Dict":
            receiver.value = args[0].eval(ctx).value
        else:
            [arg.eval(ctx) for arg in args]
            receiver.value = ctx.attrs
        return receiver

    # General Operations

    @method()
    def getitem(self, receiver, context, m, key):
        return receiver.value[key.eval(context)]

    @method()
    def setitem(self, receiver, context, m, key, value):
        receiver.value[key.eval(context)] = value.eval(context)
        return receiver

    @method()
    def delitem(self, receiver, context, m, key):
        del receiver.value[key.eval(context)]
        return receiver

    @method()
    def keys(self, receiver, context, m):
        return runtime.find("List").clone(receiver.value.keys())

    @method()
    def items(self, receiver, context, m):
        List = runtime.find("List")
        items = [List.clone([k, v]) for k, v in receiver.value.items()]
        return runtime.find("List").clone(items)

    @method()
    def values(self, receiver, context, m):
        return runtime.find("List").clone(receiver.value.values())

    @method()
    def len(self, receiver, context, m):
        return runtime.find("Number").clone(len(receiver.value))
