from mio import runtime
from mio.utils import method

from mio.object import Object

from list import List
from number import Number
from string import String


class File(Object):

    def __init__(self, value=None):
        super(File, self).__init__(value=value)

        self.update_status()

        self.create_methods()
        self["parent"] = runtime.state.find("Object")

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
        if isinstance(self.value, file):
            mode = self.value.mode
            closed = self.value.closed
            filename = self.value.name

            self["mode"] = String(filename)
            self["filename"] = String(mode)

            if closed:
                self["closed"] = runtime.state.find("True")
            else:
                self["closed"] = runtime.state.find("False")
        else:
            del self["mode"]
            del self["closed"]
            del self["filename"]

    # General Operations

    @method()
    def close(self, receiver, context, m):
        self.value.close()
        self.value = None
        self.update_status()
        return self

    @method()
    def open(self, receiver, context, m, filename, mode=None):
        filename = str(filename.eval(context))
        mode = str(mode.eval(context)) if mode else "r"
        self.value = open(filename, mode)
        self.update_status()
        return self

    @method()
    def read(self, receiver, context, m):
        return String(self.value.read())

    @method()
    def readline(self, receiver, context, m):
        return String(self.value.readline())

    @method()
    def readlines(self, receiver, context, m):
        lines = [String(line) for line in self.value.readlines()]
        return List(lines)

    @method()
    def seek(self, receiver, context, m, offset, whence=0):
        whence = int(whence.eval(context)) if whence else 0
        self.value.seek(int(offset.eval(context)), whence)
        return self

    @method()
    def pos(self, receiver, context, m):
        return Number(self.value.tell())

    @method()
    def truncate(self, receiver, context, m, size=None):
        size = int(size.eval(context)) if size else self.value.tell()
        self.value.truncate(size)
        return self

    @method()
    def write(self, receiver, context, m, data):
        data = str(data.eval(context))
        self.value.write(data)
        return self

    @method()
    def writelines(self, receiver, context, m, lines):
        lines = [str(line.eval(context)) for line in lines]
        self.value.writelines(lines)
        return self
