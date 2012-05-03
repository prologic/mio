import mio
import sys

from mio.utils import Null
from mio.object import Object
from mio.pymethod import pymethod

from mio.core.file import File


class System(Object):

    def __init__(self, value=Null, parent=None):
        super(System, self).__init__(value=value, parent=parent)

        self["args"] = self.build_args()
        self["version"] = self["String"].clone(mio.__version__)

        self["stdin"] = File(sys.stdin, parent=self["parent"])
        self["stdout"] = File(sys.stdout, parent=self["parent"])
        self["stderr"] = File(sys.stderr, parent=self["parent"])

    def build_args(self):
        String = self["String"]
        args = [String.clone(arg) for arg in sys.argv[1:]]
        return self["List"].clone(args)

    @pymethod()
    def exit(self, status=0):
        raise SystemExit(status)
