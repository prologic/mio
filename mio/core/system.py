import mio
import sys

from mio import runtime
from mio.utils import method

from mio.object import Object
from mio.core.file import File

from list import List
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
        return List([String(arg) for arg in sys.argv[1:]])

    @method()
    def exit(self, env, status=0):
        raise SystemExit(status)
