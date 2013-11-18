import sys


import mio
from mio import runtime
from mio.utils import method
from mio.object import Object


from .file import File


class System(Object):

    def __init__(self):
        super(System, self).__init__()

        self["args"] = self.build_args()
        self["version"] = runtime.find("String").clone((mio.__version__))

        self["stdin"] = File(sys.stdin)
        self["stdout"] = File(sys.stdout)
        self["stderr"] = File(sys.stderr)

        self.create_methods()
        self.parent = runtime.find("Object")

    def build_args(self):
        return runtime.find("List").clone([runtime.find("String").clone(arg) for arg in runtime.state.args])

    @method()
    def exit(self, receiver, context, m, status=None):
        status = status.eval(context) if status is not None else 0
        raise SystemExit(status)
