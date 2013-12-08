from __future__ import print_function

from os import environ
from decimal import Decimal

from .errors import Error
from .version import version


def check_parens(s):
    return s.count("(") == s.count(")")


def print_traceback(e):
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


class Completer(object):

    def __init__(self, state):
        super(Completer, self).__init__()

        self.state = state

        # Build up Global Objects
        self.objects = self.state.root.attrs.keys()
        self.objects.extend(self.state.root["Types"].attrs.keys())
        self.objects.extend(self.state.root["Core"].attrs.keys())
        if "builtins" in self.state.root:
            self.objects.extend(self.state.root["builtins"].attrs.keys())

    def complete(self, text, state):
        if state == 0:
            if " " in text:
                self.matches = self.attr_matches(text)
            else:
                self.matches = self.global_matches(text)

        try:
            return self.matches[state]
        except IndexError:
            return None

    def display_matches(self, substitution, matches, longest_match_length):
        import readline

        line_buffer = readline.get_line_buffer()
        columns = environ.get("COLUMNS", 80)

        print()

        tpl = "{:<" + str(int(max(map(len, matches)) * 1.2)) + "}"

        buffer = ""
        for match in matches:
            match = tpl.format(match[len(substitution):])
            if len(buffer + match) > columns:
                print(buffer)
                buffer = ""
            buffer += match

        if buffer:
            print(buffer)

        print(self.state.prompt, end="")
        print(line_buffer, end="")

    def global_matches(self, text):
        matches = []
        n = len(text)
        for word in self.objects:
            if word[:n] == text:
                matches.append(word)
        return matches

    def attr_matches(self, text):
        tokens = text.split(" ")
        expr, attr = " ".join(tokens[:-1]), tokens[-1]

        try:
            object = self.state.eval(expr, showerror=False, reraise=True)
        except Exception:
            return []

        words = object.attrs.keys()

        matches = []
        n = len(attr)
        for word in words:
            if word[:n] == attr:
                matches.append("{0:s} {1:s}".format(expr, word))
        return matches


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

        self.prompt = "mio> "

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
            if mapto in ("True", "False", "None"):
                return self.find(mapto)
            return self.find(mapto).clone(x)

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

    def eval(self, code, receiver=None, context=None, showerror=True, reraise=False):
        from .parser import parse
        from .lexer import tokenize

        message = None

        try:
            message = parse(tokenize(code))
            return message.eval(self.root if receiver is None else receiver, self.root if context is None else context, message)
        except Error as e:
            if showerror:
                print_traceback(e)
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
            readline.parse_and_bind("tab: complete")

            completer = Completer(self)
            readline.set_completer_delims("")
            readline.set_completer(completer.complete)
            readline.set_completion_display_matches_hook(completer.display_matches)

        print("mio {0:s}".format(version))

        code = ""
        cont = False

        while True:
            try:
                if cont:
                    self.prompt = ".... "
                else:
                    self.prompt = "mio> "

                code += raw_input(self.prompt)

                if code:
                    if check_parens(code):
                        self.runsource(code)
                        code = ""
                        cont = False
                    else:
                        cont = True
            except EOFError:
                raise SystemExit(0)
