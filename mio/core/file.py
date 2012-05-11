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
    def close(self, env):
        self.value.close()
        self.value = None
        self.update_status()
        return self

    @method()
    def open(self, env, filename, mode="r"):
        self.value = open(filename, mode)
        self.update_status()
        return self

    @method()
    def read(self, env):
        return String(self.value.read())

    @method()
    def readline(self, env):
        return String(self.value.readline())

    @method()
    def readlines(self, env):
        lines = [String(line) for line in self.value.readlines()]
        return List(lines)

    @method()
    def seek(self, env, offset, whence=0):
        self.value.seek(offset, whence)
        return self

    @method()
    def pos(self, env):
        return Number(self.value.tell())

    @method()
    def truncate(self, env, size=None):
        size = int(size) if size else self.value.tell()
        self.value.truncate(size)
        return self

    @method()
    def write(self, env, data):
        self.value.write(data)
        return self

    @method()
    def writelines(self, env, lines):
        self.value.writelines(lines)
        return self
