from mio.utils import Null
from mio.object import Object
from mio.pymethod import pymethod


class File(Object):

    def __init__(self, value=Null, parent=None):
        super(File, self).__init__(value=value, parent=parent)

        self._update_status()

    def __iter__(self):
        return self

    def next(self):
        data = self.value.read()
        if data:
            return self.lobby("String").clone(data)
        else:
            raise StopIteration

    def __repr__(self):
        if isinstance(self.value, file):
            filename, mode = self.value.name, self.value.mode
            return "File(%s, %s)" % (filename, mode)
        return super(File, self).__repr__()

    __str__ = __repr__

    def _update_status(self):
        True = self.lobby("True")
        False = self.lobby("False")
        String = self.lobby("String")

        if isinstance(self.value, file):
            self["mode"] = String.clone(self.value.mode)
            self["filename"] = String.clone(self.value.name)
            self["closed"] = True if self.value.closed else False
        else:
            del self["mode"]
            del self["closed"]
            del self["filename"]

    # General Operations

    @pymethod()
    def close(self):
        self.value.close()
        self.value = Null
        self._update_status()
        return self

    @pymethod()
    def open(self, filename, mode="r"):
        self.value = open(str(filename), str(mode))
        self._update_status()
        return self

    @pymethod()
    def read(self):
        return self.lobby("String").clone(self.value.read())

    @pymethod()
    def readline(self):
        return self.lobby("String").clone(self.value.readline())

    @pymethod()
    def readlines(self):
        List = self.lobby("List")
        String = self.lobby("String")
        lines = [String.clone(line) for line in self.value.readlines()]
        return List.clone(lines)

    @pymethod()
    def seek(self, offset, whence=0):
        self.value.seek(offset, whence)
        return self

    @pymethod()
    def pos(self):
        return self.lobby("Number").clone(self.value.tell())

    @pymethod()
    def truncate(self, size=None):
        size = size or self.value.tell()
        self.value.truncate(size)
        return self

    @pymethod()
    def write(self, data):
        self.value.write(str(data))
        return self

    @pymethod()
    def writelines(self, lines):
        lines = [str(line) for line in lines]
        self.value.writelines(lines)
        return self
