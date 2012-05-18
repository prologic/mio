import mio
import sys

from mio import runtime
from mio.utils import pymethod

from mio.object import Object

from list import List
from file import File
from string import String


class System(Object):

    def __init__(self):
        super(System, self).__init__()

        self["args"] = self.build_args()
        self["version"] = String(mio.__version__)

        self["stdin"] = File(sys.stdin)
        self["stdout"] = File(sys.stdout)
        self["stderr"] = File(sys.stderr)

        self.create_methods()
        self["parent"] = runtime.state.find("Object")

    def build_args(self):
        return List([String(arg) for arg in runtime.state.args])

    @pymethod()
    def exit(self, receiver, context, m, status=None):
        status = status.eval(context) if status is not None else 0
        raise SystemExit(status)
