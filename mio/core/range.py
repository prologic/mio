from mio.utils import Null
from mio.object import Object
from mio.pymethod import pymethod


class Range(Object):

    def __iter__(self):
        return self

    def next(self):
        return self.value.next()

    def __repr__(self):
        if self.value is not Null:
            return repr(self.value)
        return super(Range, self).__repr__()

    __str__ = __repr__

    @pymethod()
    def init(self, *args):
        self.value = range(*args)
