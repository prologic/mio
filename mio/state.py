from __future__ import print_function

from decimal import Decimal
from traceback import format_exc


from .errors import Error
from .version import version
from .utils import tryimport
from .parser import parse, tokenize

from .core import Core
from .types import Types
from .object import Object


def fromDict(x):
    return dict(x.value)


def fromBoolean(x):
    if x.value is None:
        return None
    return bool(x.value)


def toBoolean(x):
    return "True" if x else "False"


typemap = {
    "tomio": {
        dict:       "Dict",
        list:       "List",
        str:        "String",
        bool:       toBoolean,
        int:        "Number",
        type(None): "None",
        float:      "Number",
        Decimal:    "Number",
    },
    "frommio": {
        "Dict":    fromDict,
        "List":    list,
        "String":  str,
        "Boolean": fromBoolean,
        "Number":  float
    }
}


class State(object):

    def __init__(self, args, opts):
        super(State, self).__init__()

        self.args = args
        self.opts = opts

        self.root = Object(methods=False)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def create_objects(self):
        root = self.root
        object = Object()
        root.parent = object
        root["Root"] = root
        root["Object"] = object

        root["Types"] = Types()
        root["Core"] = Core()

        # Bootstrap the system
        if self.opts is None or (self.opts is not None and not self.opts.nosys):
            self.eval("""Importer import("bootstrap")""")

        # Reset the last value
        del self.root["_"]

    def frommio(self, x, default=None):
        return typemap["frommio"].get(x.type, lambda x: default)(x)

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
        if "Types" in self.root and name in self.root["Types"]:
            return self.root["Types"][name]
        elif "Core" in self.root and name in self.root["Core"]:
            return self.root["Core"][name]
        elif "builtins" in self.root and name in self.root["builtins"]:
            return self.root["builtins"][name]
        else:
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
                    if result is not None:  # pragma: no cover
                        if isinstance(result, Object):
                            output = self.eval("repr()", receiver=result)
                        else:
                            output = repr(result)
                        print("==> {0:s}".format(output))
            except EOFError:  # pragma: no cover
                raise SystemExit(0)
