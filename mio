#!/usr/bin/env python

import readline
from optparse import OptionParser
from signal import signal, SIGINT, SIG_IGN

from errors import Error
from bootstrap import Lobby
from parser import tokenize, parse

__version__ = "0.1"

USAGE = "%prog [options] ... [-c cmd | file | -] [arg] ..."
VERSION = "%prog v" + __version__

modules = (
        "lib/boolean.mio",
        "lib/if.mio",
)


class Mio:

    def __init__(self, opts):
        self.opts = opts

        #3elf.load_modules()

    def load_modules(self):
        for module in modules:
            self.load(module)

    def eval(self, code):
        message = parse(tokenize(code))
        if self.opts.debug:
            print(message.pprint())

        try:
            return message(Lobby)
        except Error as e:
            return e

    def load(self, filename):
        self.eval(open(filename, "r").read())


def parse_options():
    parser = OptionParser(usage=USAGE, version=VERSION)

    parser.add_option("-c", "",
            action="store", default=None, dest="cmd", metavar="cmd",
            help="program passed in as string (terminates option list)")

    parser.add_option("-d", "",
            action="store_true", default=False, dest="debug",
            help="debug output from parser; also MIODEBUG=x")

    opts, args = parser.parse_args()

    return opts, args


def main():
    opts, args = parse_options()

    signal(SIGINT, SIG_IGN)

    mio = Mio(opts)

    if args:
        print(mio.load(args[0]))
    else:
        readline.clear_history()
        print("mio %s" % __version__)
        while True:
            try:
                print("==> %s" % mio.eval(raw_input(">>> ")))
            except EOFError, KeyboardInterrupt:
                raise SystemExit(0)

if __name__ == "__main__":
    main()
