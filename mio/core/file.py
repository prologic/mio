from mio.object import Object
from mio.pymethod import pymethod


class File(Object):

    def __iter__(self):
        String = self.lobby("String")
        for line in self.value:
            yield String.clone(line)

    def __repr__(self):
        if isinstance(self.value, file):
            filename, mode = self.value.name, self.value.mode
            return "File(%s, %s)" % (filename, mode)
        return super(File, self).__repr__()

    __str__ = __repr__

    # General Operations

    @pymethod()
    def open(self, filename, mode="r"):
        self.value = open(filename, mode)
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

    # Type Conversion

    @pymethod()
    def repr(self):
        return self.lobby("String").clone(repr(self))
