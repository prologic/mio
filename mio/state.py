from __future__ import print_function

from decimal import Decimal
from traceback import format_exc


from funcy import constantly


from .errors import Error
from .version import version
from .utils import tryimport
from .parser import parse, tokenize

from .block import Block
from .object import Object
from .parser import Parser
from .message import Message
from .continuation import Continuation

from .core import Boolean
from .core import Number
from .core import String
from .core import List
from .core import Dict
from .core import FFI
from .core import File
from .core import Range
from .core import System
from .core import Module
from .core import Importer


def fromDict(x):
    return dict(x.value)


def tobool(x):
    return "True" if x else "False"


typemap = {
    "tomio": {
        dict:       "Dict",
        list:       "List",
        str:        "String",
        bool:       tobool,
        int:        "Number",
        type(None): "None",
        float:      "Number",
        Decimal:    "Number",
    },
    "frommio": {
        "Dict":    fromDict,
        "List":    list,
        "String":  str,
        "Boolean": bool,
        "Number":  float
    }
}


class State(object):

    def __init__(self, args, opts, root):
        super(State, self).__init__()

        self.args = args
        self.opts = opts
        self.root = root

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def create_objects(self):
        root = self.root

        object = Object(methods=True)

        root["Root"] = root
        root["Object"] = object

        root.parent = object

        root["Boolean"] = Boolean()
        root["Number"] = Number()
        root["String"] = String()
        root["List"] = List()
        root["Dict"] = Dict()

        root["None"] = Boolean(None)
        root["True"] = Boolean(True)
        root["False"] = Boolean(False)

        root["Parser"] = Parser()
        root["Message"] = Message("")
        root["Continuation"] = Continuation()
        root["Block"] = Block(None, [], {})

        root["FFI"] = FFI()
        root["File"] = File()
        root["Range"] = Range()
        root["System"] = System()
        root["Module"] = Module()
        root["Importer"] = Importer()

    def frommio(self, x, default=None):
        return typemap["frommio"].get(x.type, constantly(default))(x)

    def tomio(self, x, default="None"):
        mapto = typemap["tomio"].get(type(x), default)

        try:
            if callable(mapto):
                return self.find(mapto(x)).clone(x)
            else:
                return self.find(mapto).clone(x)
        except:
            return default

    def find(self, name):
        return self.root[name]

    def eval(self, code, receiver=None, context=None, reraise=False):
        message = None
        try:
            return parse(tokenize(code)).eval(self.root if receiver is None else receiver, self.root if context is None else context, message)
        except Error as e:
            type = e.__class__.__name__
            underline = "-" * (len(type) + 1)
            print("\n  %s: %s\n  %s\n  %r\n" % (type, e, underline, message))
            if reraise:
                raise
        except Exception as e:  # pragma: no cover
            print("ERROR: {0:s}\n{1:s}".format(e, format_exc()))
            if reraise:
                raise

    def load(self, filename, receiver=None, context=None):
        self.eval(open(filename, "r").read(), receiver=receiver, context=context)

    def repl(self):
        tryimport("readline")

        print("mio {0:s}".format(version))

        while True:
            try:
                code = raw_input(">>> ")
                if code:
                    result = self.eval(code)
                    if result is not None and result.value is not None:  # pragma: no cover
                        print("==> {0:s}".format(self.eval("repr()", receiver=result)))
            except EOFError:  # pragma: no cover
                raise SystemExit(0)
