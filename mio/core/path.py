import posix
import posixpath


from mio import runtime
from mio.utils import method
from mio.object import Object


class Path(Object):

    def __init__(self, path=None, expanduser=False):
        super(Path, self).__init__()

        path = posix.getcwdu() if path is None else path
        self.value = posixpath.expanduser(path) if expanduser else path

        self.create_methods()
        self.parent = runtime.find("Object")

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return self.value != other.value

    def __gt__(self, other):
        return self.value > other.value

    def __lt__(self, other):
        return self.value < other.value

    def __repr__(self):
        return "Path({0:s})".format(repr(self.value))

    def __str__(self):
        return self.value

    # General Operations

    @method()
    def init(self, receiver, context, m, path=None, expanduser=False):
        path = posix.getcwdu() if path is None else str(path.eval(context))
        expanduser = False if expanduser is False else bool(expanduser.eval(context))
        receiver.value = posixpath.expanduser(path) if expanduser else path
        return receiver

    @method()
    def join(self, receiver, context, m, *args):
        args = [str(arg.eval(context)) for arg in args]
        return receiver.clone(posixpath.join(self.value, args))

    @method()
    def open(self, receiver, context, m, mode="r"):
        mode = mode if mode == "r" else str(mode.eval(context))
        assert posixpath.isfile(receiver.value)
        return runtime.state.eval("""File clone() open("{0:s}", "{1:s}")""".format(self.value, mode))

    @method()
    def list(self, receiver, context, m, fil=None, rec=False):
        fil = fil.eval(context) if fil is not None else fil
        rec = bool(rec.eval(context)) if rec is not False else rec
        paths = [receiver.clone(path) for path in posix.listdir(receiver.value)]
        return runtime.state.find("List").clone(paths)
