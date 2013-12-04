from __future__ import print_function

from decimal import Decimal


from .errors import Error
from .version import version


def check_parens(s):
    return s.count("(") == s.count(")")


class State(object):

    def __init__(self, args=None, opts=None):
        super(State, self).__init__()

        self.args = args if args is not None else []
        self.opts = opts

        self.typemap = {
            "tomio": {
                dict:       self.toDict,
                list:       self.toList,
                tuple:      self.toTuple,
                bool:       self.toBoolean,
                str:        "Bytes",
                bytes:      "Bytes",
                unicode:    "String",
                int:        "Number",
                type(None): "None",
                float:      "Number",
                Decimal:    "Number",
            },
            "frommio": {
                "Dict":    self.fromDict,
                "List":    self.fromList,
                "Tuple":   self.fromTuple,
                "Boolean": self.fromBoolean,
                "Bytes":   bytes,
                "String":  unicode,
                "Number":  float
            }
        }

    def fromDict(self, x):
        return dict((self.frommio(k), self.frommio(v)) for k, v in x.value.items())

    def fromList(self, xs):
        return list(self.frommio(x) for x in xs.value)

    def fromTuple(self, xs):
        return tuple(self.frommio(x) for x in xs.value)

    def fromBoolean(self, x):
        if x.value is None:
            return None
        return bool(x.value)

    def toDict(self, x):
        return self.find("Dict").clone(dict(((self.tomio(k), self.tomio(v)) for k, v in x.items())))

    def toList(self, xs):
        return self.find("List").clone(list((self.tomio(x) for x in xs)))

    def toTuple(self, xs):
        return self.find("Tuple").clone(tuple((self.tomio(x) for x in xs)))

    def toBoolean(self, x):
        return self.find("True") if x else self.find("False")

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def bootstrap(self):
        from .object import Object
        from .trait import Trait

        # Fake Object to solve chicken/egg problem.
        self.root = {"Object": None}

        object = Object()

        root = Object(methods=False)
        root.parent = object

        root["Object"] = object
        root["Trait"] = Trait()
        root["Root"] = root

        self.root = root

    def initialize(self):
        from .core import Core
        from .types import Types
        from .traits import Traits

        root = self.root

        root["Types"] = Types()
        root["Core"] = Core()
        root["Traits"] = Traits()

        # Bootstrap the system
        if self.opts is None or (self.opts is not None and not self.opts.nosys):
            self.eval("""Importer import("bootstrap")""")

        # Reset the last value
        del self.root["_"]

    def frommio(self, x, default=None):
        return self.typemap["frommio"].get(x.type, lambda x: default)(x)

    def tomio(self, x, default="None"):
        mapto = self.typemap["tomio"].get(type(x), default)

        if callable(mapto):
            return mapto(x)
        else:
            try:
                obj = self.find(mapto(x)) if callable(mapto) else self.find(mapto)
                return obj.clone(x)
            except KeyError:
                return default

    def find(self, name):
        if "Types" in self.root and name in self.root["Types"]:
            return self.root["Types"][name]
        elif "Core" in self.root and name in self.root["Core"]:
            return self.root["Core"][name]
        elif "Traits" in self.root and name in self.root["Traits"]:
            return self.root["Traits"][name]
        elif "builtins" in self.root and name in self.root["builtins"]:
            return self.root["builtins"][name]
        else:
            return self.root[name]

    def eval(self, code, receiver=None, context=None, reraise=False):
        from .parser import parse
        from .lexer import tokenize

        message = None

        try:
            message = parse(tokenize(code))
            return message.eval(self.root if receiver is None else receiver, self.root if context is None else context, message)
        except Error as e:
            from .object import Object
            if e.args and isinstance(e.args[0], Object):
                error = e.args[0]
                type = str(error["type"]) if error["type"] is not None else error.type
                message = str(error["message"]) if error["message"] is not None else ""
            else:
                type = e.__class__.__name__
                message = str(e)

            stack = "\n".join(["  {0:s}".format(repr(m)) for m in e.stack])
            underline = "-" * (len(type) + 1)
            print("\n  {0:s}: {1:s}\n  {2:s}\n{3:s}\n".format(type, message, underline, stack))
            if reraise:
                raise
        except Exception as e:  # pragma: no cover
            print("ERROR:", e)
            from traceback import format_exc
            print(format_exc())
            if reraise:
                raise

    def load(self, filename, receiver=None, context=None):
        self.eval(open(filename, "r").read(), receiver=receiver, context=context)

    def runsource(self, source):
        from .utils import format_result

        if not check_parens(source):
            return True

        result = self.eval(source)
        if result is not None:
            output = format_result(result)
            if output is not None:
                print("===> {0:s}".format(output))

    def repl(self):
        from .utils import tryimport

        readline = tryimport("readline")

        if readline is not None:
            objects = self.root.attrs.keys()
            objects.extend(self.root["Types"].attrs.keys())
            objects.extend(self.root["Core"].attrs.keys())
            if "builtins" in self.root:
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
                    ps = ".... "
                else:
                    ps = "mio> "

                code += raw_input(ps)

                if code:
                    if check_parens(code):
                        self.runsource(code)
                        code = ""
                        cont = False
                    else:
                        cont = True
            except EOFError:  # pragma: no cover
                raise SystemExit(0)
