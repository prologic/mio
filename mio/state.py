from traceback import format_exc

import mio
from utils import tryimport
from parser import parse, tokenize

from errors import Error

from method import Method
from object import Object
from parser import Parser
from message import Message
from continuation import Continuation

from core import Boolean
from core import Number
from core import String
from core import List

from core import File
from core import Range
from core import System


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

    def eval(self, code, reraise=False):
        message = None
        try:
            if self.opts and self.opts.debug:
                tokens = tokenize(code)
                message = parse(tokens)
                print("Tokens:\n%s\n" % repr(tokens))
                print("Messages:\n%r\n" % repr(message))
            else:
                message = parse(tokenize(code))

            return message.eval(self.lobby, self.lobby, message)
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

        print("mio %s" % mio.__version__)

        while True:
            try:
                result = self.eval(raw_input(">>> "))
                if result is not None:
                    print("==> %s" % str(result))
            except EOFError:
                raise SystemExit(0)
