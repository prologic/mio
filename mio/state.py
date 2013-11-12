from __future__ import print_function

from decimal import Decimal
from traceback import format_exc


from .errors import Error
from .parser import parse
from .lexer import tokenize
from .version import version
from .utils import format_result, tryimport

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

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def bootstrap(self):
        # Fake Object to solve chicken/egg problem.
        self.root = {"Object": None}

        object = Object()

        root = Object(methods=False)
        root.parent = object

        root["Object"] = object
        root["Root"] = root

        self.root = root

    def initialize(self):
        root = self.root

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
            obj = self.find(mapto(x)) if callable(mapto) else self.find(mapto)
            return obj.clone(x)
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
            if e.args and isinstance(e.args[0], Object):
                error = e.args[0]
                type = str(error["type"]) if error["type"] is not None else error.type
                message = str(error["message"]) if error["message"] is not None else ""
            else:
                type = e.__class__.__name__
                message = str(e)

            stack = "\n".join([repr(m) for m in e.stack])
            underline = "-" * (len(type) + 1)
            print("\n  {0:s}: {1:s}\n  {2:s}\n  {3:s}\n".format(type, message, underline, stack))
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
                code = raw_input("mio> ")
                if code:
                    result = self.eval(code)
                    if result is not None:  # pragma: no cover
                        output = format_result(result)
                        if output is not None:
                            print("===> {0:s}".format(output))
            except EOFError:  # pragma: no cover
                raise SystemExit(0)
