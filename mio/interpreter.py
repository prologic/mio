from glob import glob
from traceback import format_exc

import mio
from errors import Error
from utils import tryimport
from attrdict import AttrDict
from parser import parse, tokenize


class Interpreter:

    def __init__(self, opts, lobby, state):
        self.opts = opts
        self.lobby = lobby
        self.state = state

        self.env = AttrDict()

        for module in glob("./lib/*.mio"):
            self.load(module)

    def eval(self, code):
        if self.opts.debug:
            tokens = tokenize(code)
            message = parse(tokens)
            print("Tokens:\n%s\n" % tokens)
            print("Messages:\n%r\n" % message)
        else:
            message = parse(tokenize(code))

        try:
            self.env.update({
                "msg": message,
                "sender": self.lobby, 
                "target": self.lobby,
            })
            return message.perform_on(self.env, self.lobby, self.lobby)
        except Error as e:
            print("%s\n%r" % (e, message))

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
