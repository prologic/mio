from mio import runtime
from mio.utils import method
from mio.object import Object


class File(Object):

    def __iter__(self):
        data = self.value.read()
        while data:
            yield runtime.find("String").clone(data)
            data = self.value.read()

    def __repr__(self):
        if isinstance(self.value, file):
            filename, mode = self.value.name, self.value.mode
            state = "closed" if self.value.closed else "open"
            return "File({0:s}, mode={1:s}, state={2:s})".format(repr(filename), repr(mode), repr(state))
        return "File"

    def update_status(self):
        mode = self.value.mode
        closed = self.value.closed
        filename = self.value.name

        self["mode"] = runtime.find("String").clone(mode)
        self["filename"] = runtime.find("String").clone(filename)

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
    def flush(self, receiver, context, m):
        receiver.value.flush()
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
        return runtime.find("String").clone(receiver.value.read(size))

    @method()
    def readline(self, receiver, context, m):
        return runtime.find("String").clone(receiver.value.readline())

    @method()
    def readlines(self, receiver, context, m):
        lines = [runtime.find("String").clone(line) for line in receiver.value.readlines()]
        return runtime.find("List").clone(lines)

    @method()
    def seek(self, receiver, context, m, offset, whence=None):
        whence = int(whence.eval(context)) if whence is not None else 0
        receiver.value.seek(int(offset.eval(context)), whence)
        return receiver

    @method(property=True)
    def pos(self, receiver, context, m):
        return runtime.find("Number").clone(receiver.value.tell())

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
