from __future__ import print_function

from traceback import format_exc

from .errors import Error
from .version import version
from .utils import tryimport
from .parser import parse, tokenize

from .method import Method
from .object import Object
from .parser import Parser
from .message import Message
from .continuation import Continuation

from .types import Boolean
from .types import Number
from .types import String
from .types import List
from .types import File
from .types import Range
from .types import System


class State(object):

    def __init__(self, args, opts, lobby):
        super(State, self).__init__()

        self.args = args
        self.opts = opts
        self.lobby = lobby

        if self.args is None:
            self.args = []

        self.reset()

    def reset(self):
        self.returnValue = None
        self.isContinue = False
        self.isReturn = False
        self.isBreak = False

    def stop(self):
        return self.isBreak or self.isReturn

    def create_objects(self):
        lobby = self.lobby

        object = Object(methods=True)

        lobby["Lobby"] = lobby
        lobby["Object"] = object

        lobby.parent = object

        lobby["Boolean"] = Boolean()
        lobby["Number"] = Number()
        lobby["String"] = String()
        lobby["List"] = List()

        lobby["None"] = Boolean(None)
        lobby["True"] = Boolean(True)
        lobby["False"] = Boolean(False)

        lobby["Parser"] = Parser()
        lobby["Message"] = Message("")
        lobby["Continuation"] = Continuation()
        lobby["Method"] = Method(None, Message(""), [], {})

        lobby["File"] = File()
        lobby["Range"] = Range()
        lobby["System"] = System()

    def find(self, name):
        return self.lobby.attrs[name]

    def eval(self, code, receiver=None, context=None, reraise=False):
        message = None
        try:
            if self.opts and self.opts.debug:
                tokens = tokenize(code)
                message = parse(tokens)
                print("Tokens:\n%s\n" % tokens)
                print("Messages:\n%r\n" % message)
            else:
                message = parse(tokenize(code))

            return message.eval(self.lobby if receiver is None else receiver, self.lobby if context is None else context, message)
        except Error as e:
            type = e.__class__.__name__
            underline = "-" * (len(type) + 1)
            print("\n  %s: %s\n  %s\n  %r\n" % (type, e, underline, message))
            if reraise:
                raise
        except Exception as e:
            print("%s\n%s" % (e, format_exc()))
            if reraise:
                raise

    def load(self, filename):
        try:
            self.eval(open(filename, "r").read())
        except Exception as e:
            print("ERROR: %s" % e)
            print(format_exc())

    def repl(self):
        tryimport("readline")

        print("mio {0:s}".format(version))

        while True:
            try:
                code = raw_input(">>> ")
                if code:
                    result = self.eval(code)
                    if result is not None:
                        print("==> {0:s}".format(self.eval("repr", receiver=result)))
            except EOFError:
                raise SystemExit(0)
