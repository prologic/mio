#!/usr/bin/env python

from optparse import OptionParser
from signal import signal, SIGINT, SIG_IGN

from mio.errors import Error
from mio.utils import tryimport
from mio.bootstrap import Lobby
from mio.parser import tokenize, parse

__version__ = "0.1"

USAGE = "%prog [options] ... [-c cmd | file | -] [arg] ..."
VERSION = "%prog v" + __version__

modules = (
        "lib/operators.mio",
        "lib/boolean.mio",
        "lib/if.mio",
)


class Mio:

    def __init__(self, opts):
        self.opts = opts

        self.load_modules()

    def load_modules(self):
        for module in modules:
            self.load(module)

    def eval(self, code):
        if self.opts.debug:
            tokens = tokenize(code)
            message = parse(tokens)
            print("Tokens:\n%s\n" % tokens)
            print("Messages:\n%s\n" % message.pprint())
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

        print("mio %s" % __version__)

        while True:
            try:
                print("==> %r" % self.eval(raw_input(">>> ")))
            except (EOFError, KeyboardInterrupt):
                raise SystemExit(0)


def parse_options():
    parser = OptionParser(usage=USAGE, version=VERSION)

    parser.add_option("-c", "",
            action="store", default=None, dest="cmd", metavar="cmd",
            help="program passed in as string (terminates option list)")

    parser.add_option("-i", "",
            action="store_true", default=False, dest="inspect",
            help="inspect interactively after running script")

    parser.add_option("-d", "",
            action="store_true", default=False, dest="debug",
            help="debug output from parser; also MIODEBUG=x")

    opts, args = parser.parse_args()

    return opts, args


def main():
    opts, args = parse_options()

    signal(SIGINT, SIG_IGN)

    mio = Mio(opts)

    if opts.cmd:
        print(repr(mio.eval(opts.cmd)))
    elif args:
        mio.load(args[0])
        if opts.inspect:
            mio.repl()
    else:
        mio.repl()

if __name__ == "__main__":
    main()
