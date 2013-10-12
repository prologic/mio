from mio import runtime
from mio.utils import method

from mio.object import Object

from list import List
from number import Number
from string import String


class File(Object):

    def __init__(self, value=None):
        super(File, self).__init__(value=value)

        self.create_methods()
        self.parent = runtime.state.find("Object")

    def __iter__(self):
        data = self.value.read()
        while data:
            yield String(data)
            data = self.value.read()

    def __str__(self):
        if isinstance(self.value, file):
            filename, mode = self.value.name, self.value.mode
            return "File(%s, %s)" % (filename, mode)
        return super(File, self).__str__()

    def update_status(self):
        mode = self.value.mode
        closed = self.value.closed
        filename = self.value.name

        self["mode"] = String(mode)
        self["filename"] = String(filename)

        if closed:
            self["closed"] = runtime.find("True")
        else:
            self["closed"] = runtime.find("False")

    # General Operations

    @method()
    def close(self, receiver, context, m):
        receiver.value.close()
        receiver.update_status()
        return receiver

    @method()
    def open(self, receiver, context, m, filename, mode=None):
        filename = str(filename.eval(context))
        mode = str(mode.eval(context)) if mode is not None else "r"
        receiver.value = open(filename, mode)
        receiver.update_status()
        return receiver

    @method()
    def read(self, receiver, context, m, size=None):
        size = int(size.eval(context)) if size is not None else -1
        return String(receiver.value.read(size))

    @method()
    def readline(self, receiver, context, m):
        return String(receiver.value.readline())

    @method()
    def readlines(self, receiver, context, m):
        lines = [String(line) for line in receiver.value.readlines()]
        return List(lines)

    @method()
    def seek(self, receiver, context, m, offset, whence=None):
        whence = int(whence.eval(context)) if whence is not None else 0
        receiver.value.seek(int(offset.eval(context)), whence)
        return receiver

    @method()
    def pos(self, receiver, context, m):
        return Number(receiver.value.tell())

    @method()
    def truncate(self, receiver, context, m, size=None):
        size = int(size.eval(context)) if size else receiver.value.tell()
        receiver.value.truncate(size)
        return receiver

    @method()
    def write(self, receiver, context, m, data):
        data = str(data.eval(context))
        receiver.value.write(data)
        return receiver

    @method()
    def writelines(self, receiver, context, m, data):
        lines = [str(line) for line in data.eval(context)]
        receiver.value.writelines(lines)
        return receiver
