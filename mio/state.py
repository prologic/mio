from __future__ import print_function

from traceback import format_exc


from .errors import Error
from .version import version
from .utils import tryimport
from .parser import parse, tokenize

from .block import Block
from .object import Object
from .parser import Parser
from .message import Message
from .continuation import Continuation

from .types import Boolean
from .types import Number
from .types import String
from .types import List
from .types import Dict
from .types import File
from .types import Range
from .types import System


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

        root["File"] = File()
        root["Range"] = Range()
        root["System"] = System()

        root["_"] = root["None"]

    def find(self, name):
        return self.root.attrs[name]

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

    def load(self, filename):
        self.eval(open(filename, "r").read())

    def repl(self):
        tryimport("readline")

        print("mio {0:s}".format(version))

        while True:
            try:
                code = raw_input(">>> ")
                if code:
                    result = self.eval(code)
                    if result is not None and result.value is not None:# pragma: no cover
                        print("==> {0:s}".format(self.eval("repr", receiver=result)))
            except EOFError:  # pragma: no cover
                raise SystemExit(0)
