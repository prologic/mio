import sys


import mio
from mio import runtime
from mio.object import Object
from mio.utils import method, Null


class System(Object):

    def __init__(self, value=Null):
        super(System, self).__init__(value=value)

        self["args"] = self.build_args()
        self["version"] = runtime.find("String").clone((mio.__version__))

        self["stdin"] = runtime.find("File").clone(sys.stdin)
        self["stdout"] = runtime.find("File").clone(sys.stdout)
        self["stderr"] = runtime.find("File").clone(sys.stderr)

        self.create_methods()
        self.parent = runtime.find("Object")

    def build_args(self):
        return runtime.find("List").clone([runtime.find("String").clone(arg) for arg in runtime.state.args])

    @method()
    def exit(self, receiver, context, m, status=None):
        status = status.eval(context) if status is not None else 0
        raise SystemExit(status)
