from traceback import format_exc

import mio
from utils import tryimport
from parser import parse, tokenize

from errors import Error

from block import Block
from object import Object
from message import Message

from core import Number
from core import String
from core import List
from core import Map

from core import File
from core import Range
from core import System


class State(object):

    STATES = ("isBreak", "isReturn",)

    def __init__(self, opts, lobby):
        super(State, self).__init__()

        self.opts = opts
        self.lobby = lobby

        self.reset()

    def reset(self):
        self.returnValue = None
        self.isContinue = False
        self.isReturn = False
        self.isBreak = False

    def stop(self):
        return any([getattr(self, k, False) for k in self.STATES])

    def create_objects(self):
        lobby = self.lobby

        object = Object(methods=True)

        lobby["Lobby"] = lobby
        lobby["Object"] = object

        lobby["type"] = String("Lobby")
        lobby["parent"] = object

        lobby["Number"] = Number()
        lobby["String"] = String()
        lobby["List"] = List()
        lobby["Map"] = Map()

        lobby["None"] = object.clone(None)
        lobby["True"] = object.clone(True)
        lobby["False"] = object.clone(False)

        lobby["Block"] = Block(lobby, Message(""), [])
        lobby["Message"] = Message("")

        lobby["File"] = File()
        lobby["Range"] = Range()
        lobby["System"] = System()

    def find(self, name):
        return self.lobby.attrs[name]

    def eval(self, code):
        try:
            if self.opts and self.opts.debug:
                tokens = tokenize(code)
                message = parse(tokens)
                print("Tokens:\n%s\n" % tokens)
                print("Messages:\n%r\n" % message)
            else:
                message = parse(tokenize(code))

            return message.eval(self.lobby, self.lobby, message)
        except Error as e:
            print("%s\n%r" % (e, message))
        except Exception as e:
            print("%s\n%s" % (e, format_exc()))

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
                print("==> %s" % str(self.eval(raw_input(">>> "))))
            except EOFError:
                raise SystemExit(0)
