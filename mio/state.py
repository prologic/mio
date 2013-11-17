from __future__ import print_function

from decimal import Decimal


from .errors import Error
from .version import version


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


def check_parens(s):
    return s.count("(") == s.count(")")


class State(object):

    def __init__(self, args=None, opts=None):
        super(State, self).__init__()

        self.args = args if args is not None else []
        self.opts = opts

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def bootstrap(self):
        from .object import Object

        # Fake Object to solve chicken/egg problem.
        self.root = {"Object": None}

        object = Object()

        root = Object(methods=False)
        root.parent = object

        root["Object"] = object
        root["Root"] = root

        self.root = root

    def initialize(self):
        from .core import Core
        from .types import Types

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
        from .parser import parse
        from .lexer import tokenize

        message = None

        try:
            return parse(tokenize(code)).eval(self.root if receiver is None else receiver, self.root if context is None else context, message)
        except Error as e:
            from .object import Object
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
            print("ERROR:", e)
            if reraise:
                raise

    def load(self, filename, receiver=None, context=None):
        self.eval(open(filename, "r").read(), receiver=receiver, context=context)

    def repl(self):
        from .utils import format_result, tryimport

        readline = tryimport("readline")

        if readline is not None:
            objects = self.root.attrs.keys()
            objects.extend(self.root["Types"].attrs.keys())
            objects.extend(self.root["Core"].attrs.keys())
            objects.extend(self.root["builtins"].attrs.keys())

            def completer(text, state):
                options = [i for i in objects if i.startswith(text)]
                if state < len(options):
                    return options[state]
                else:
                    return None

            readline.parse_and_bind("tab: complete")
            readline.set_completer(completer)

        print("mio {0:s}".format(version))

        code = ""
        cont = False

        while True:
            try:
                if cont:
                    ps = "..... "
                else:
                    ps = "mio> "

                code += raw_input(ps)

                if code:
                    if check_parens(code):
                        result = self.eval(code)
                        if result is not None:  # pragma: no cover
                            output = format_result(result)
                            if output is not None:
                                print("===> {0:s}".format(output))
                        code = ""
                        cont = False
                    else:
                        cont = True
            except EOFError:  # pragma: no cover
                raise SystemExit(0)
