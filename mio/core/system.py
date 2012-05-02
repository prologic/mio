import mio
import sys

from mio.utils import Null
from mio.object import Object
from mio.pymethod import pymethod


class System(Object):

    def __init__(self, value=Null, parent=None):
        super(System, self).__init__(value=value, parent=parent)

        self["args"] = self.build_args()
        self["version"] = self.lobby("String").clone(mio.__version__)

    def build_args(self):
        String = self.lobby("String")
        args = [String.clone(arg) for arg in sys.argv]
        return self.lobby("List").clone(args)

    @pymethod()
    def exit(self, status=0):
        raise SystemExit(status)
