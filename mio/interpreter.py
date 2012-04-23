from glob import glob

import mio
from errors import Error
from bootstrap import Lobby
from utils import tryimport
from parser import parse, tokenize


class Interpreter:

    def __init__(self, opts):
        self.opts = opts

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
            return message(Lobby)
        except Error as e:
            print("%s\n%r" % (str(e), message))

    def load(self, filename):
        self.eval(open(filename, "r").read())

    def repl(self):
        tryimport("readline")

        print("mio %s" % mio.__version__)

        while True:
            try:
                print("==> %r" % self.eval(raw_input(">>> ")))
            except (EOFError, KeyboardInterrupt):
                raise SystemExit(0)
